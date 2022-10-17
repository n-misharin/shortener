import pytest

from shortener.utils import make_short, get_url_by_long, add_url, make_vip
from shortener.utils.make_shorter import ExistURLException


class TestMakeShort:
    @staticmethod
    def get_work_site_url():
        return "https://fastapi.tiangolo.com/"

    async def test_add_url(self, database):
        url1 = await add_url(database, TestMakeShort.get_work_site_url(), "hello")
        url2 = await get_url_by_long(database, TestMakeShort.get_work_site_url())
        assert url1 == url2

    async def test_make_short(self, database):
        url = await make_short(database, TestMakeShort.get_work_site_url())
        db_url = await get_url_by_long(database, TestMakeShort.get_work_site_url())
        assert url == db_url

    async def test_duplicate_make_short(self, database):
        url1 = await make_short(database, TestMakeShort.get_work_site_url())
        url2 = await make_short(database, TestMakeShort.get_work_site_url())
        assert url1 == url2

    async def test_make_vip(self, database):
        url = await make_vip(database, TestMakeShort.get_work_site_url(), "VIP")
        db_url = await get_url_by_long(database, TestMakeShort.get_work_site_url())
        assert url == db_url

    async def test_busy_suffix_make_vip(self, database):
        suffix1 = "VIP"
        suffix2 = "NOT_VIP"
        url1 = await make_vip(database, TestMakeShort.get_work_site_url(), suffix1)
        url2 = await make_vip(database, TestMakeShort.get_work_site_url(), suffix2)
        assert url2.short_url == suffix1
        assert url1 == url2
        with pytest.raises(ExistURLException) as excinfo:
            await make_vip(database, "https://vk.com", "VIP")


