from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.database import *

router = Router()


def split_people(table, column_name, schedule):
    get = get_records(table, column_name)

    result = []
    index = 0
    schedule_lines = schedule.splitlines()

    for line in schedule_lines:
        if '—' in line and index < 0:
            result.append(f"{line} {get[index]}")
            index += 1
        else:
            result.append(line)

    return result


class AddUserState(StatesGroup):
    waiting_for_hosts = State()
    waiting_for_djs = State()
    waiting_for_cohosts = State()
    waiting_for_schedule = State()


def register_handlers(dp, bot):
    dp.include_router(router)

    @router.message(CommandStart())
    async def cmd_start(message: Message):
        await message.answer(
            'Зато не надо ждать')

    @router.message(Command('hosts'))
    async def cmd_hosts(message: Message, state: FSMContext) -> None:
        await state.set_state(AddUserState.waiting_for_hosts)

    @router.message(AddUserState.waiting_for_hosts)
    async def add_host_handler(message: Message, state: FSMContext) -> None:
        host_names = message.text.strip().splitlines()

        for host in host_names:
            host = host.strip()
            if host:
                add_host(host)

        await message.answer('Список ведущих сохранён.')
        await state.clear()

    @router.message(Command('djs'))
    async def cmd_djs(message: Message, state: FSMContext) -> None:
        await state.set_state(AddUserState.waiting_for_djs)

    @router.message(AddUserState.waiting_for_djs)
    async def add_dj_handler(message: Message, state: FSMContext) -> None:
        dj_names = message.text.strip().splitlines()

        for dj in dj_names:
            dj = dj.strip()
            if dj:
                add_dj(dj)

        await message.answer('Список диджеев сохранён.')
        await state.clear()

    @router.message(Command('cohosts'))
    async def cmd_cohosts(message: Message, state: FSMContext) -> None:
        await state.set_state(AddUserState.waiting_for_cohosts)

    @router.message(AddUserState.waiting_for_cohosts)
    async def add_cohost_handler(message: Message, state: FSMContext) -> None:
        cohost_names = message.text.strip().splitlines()

        for cohost in cohost_names:
            cohost = cohost.strip()
            if cohost:
                add_cohost(cohost)

        await message.answer('Список соведущих сохранён.')
        await state.clear()

    @router.message(Command('schedule'))
    async def cmd_schedule(message: Message, state: FSMContext) -> None:
        await state.set_state(AddUserState.waiting_for_schedule)

    @router.message(AddUserState.waiting_for_schedule)
    async def add_schedule_handler(message: Message, state: FSMContext) -> None:
        schedule = message.text
        add_record('schedule', 'schedule', schedule)

        await state.clear()

    @router.message(Command('update'))
    async def cmd_update(message: Message, state: FSMContext) -> None:
        schedule = get_schedule()
        if not schedule:
            await message.answer('Нет расписания.')
            return

        hosts = get_hosts()
        djs = get_djs()
        cohosts = get_cohosts()

        if not hosts or not djs or not cohosts:
            await message.answer('Не все есть в расписании.')
            return

        host_index, dj_index, cohost_index = 0, 0, 0

        schedule_lines = schedule.splitlines()
        updated_schedule = []

        for line in schedule_lines:
            if '—' in line:
                current_host = hosts[host_index % len(hosts)]
                current_dj = djs[dj_index % len(djs)]
                current_cohost = cohosts[cohost_index % len(cohosts)]

                updated_line = f"{line} {current_host}, {current_dj}, {current_cohost}"
                updated_schedule.append(updated_line)

                host_index += 1
                dj_index += 1
                cohost_index += 1
            else:
                updated_schedule.append(line)

        final_schedule = '\n'.join(updated_schedule)
        delete_schedule()
        add_record('schedule', 'schedule', final_schedule)

        await message.answer(final_schedule)

    @router.message(Command('clear'))
    async def cmd_clear(message: Message):
        clear_all()
        await message.answer("Все данные очищены.")
