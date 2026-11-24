import pytest
from datetime import date, timedelta
from playwright.sync_api import Page, expect

def test_successful_booking(page: Page, base_url: str):
    page.goto(base_url)
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    page.locator("#date").fill(tomorrow)
    page.locator("#room").select_option("small")
    page.locator("#start-time").fill("10:00")
    page.locator("#end-time").fill("11:00")
    page.locator("#participants").fill("4")
    page.locator("#name").fill("Sergey")
    page.locator("#email").fill("sergey@example.com")
    page.get_by_role("button", name="Забронировать").click()
    expect(page.locator("#form-status")).to_contain_text("Бронирование создано")
    expect(page.locator("#form-status")).to_contain_text("Малая")
    expect(page.locator("#form-status")).to_contain_text("Sergey")


def test_invalid_booking(page: Page, base_url: str):
    page.goto(base_url)

    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    page.locator("#date").fill(tomorrow)
    page.locator("#room").select_option("small")
    page.locator("#start-time").fill("10:00")
    page.locator("#end-time").fill("11:00")
    page.locator("#participants").fill("5")
    page.locator("#name").fill("Sergey")
    page.locator("#email").fill("sergey@example.com")

    page.get_by_role("button", name="Забронировать").click()

    expect(page.locator("#form-status")).to_contain_text(
        "Проверьте, пожалуйста, заполнение формы."
    )
    expect(page.locator('[name="participants"]')
           .locator("xpath=..")
           .locator(".field-error")).to_have_text(
        "В комнате максимум 4 участника."
    )

@pytest.mark.xfail(
    strict=True,
    reason="Баг №1: приложение принимает бронирование длительностью менее 30 минут",
    raises=AssertionError
)
def test_discovered_defect(page: Page, base_url: str):
    page.goto(base_url)

    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    page.locator("#date").fill(tomorrow)
    page.locator("#room").select_option("small")
    page.locator("#start-time").fill("10:00")
    page.locator("#end-time").fill("10:01")
    page.locator("#participants").fill("2")
    page.locator("#name").fill("Sergey")
    page.locator("#email").fill("sergey@example.com")

    page.get_by_role("button", name="Забронировать").click()

    expect(page.locator("#form-status")).to_contain_text(
        "Проверьте, пожалуйста, заполнение формы."
    )

