"""Test that BrowserProfile.get_args() preserves the CHROME_DEFAULT_ARGS ordering.

Regression test for: get_args() converted CHROME_DEFAULT_ARGS to a set when
ignore_default_args was a list, so the remaining default args came back in an
arbitrary order that varied between Python processes (hash-seed dependent).
"""

from browser_use.browser.profile import CHROME_DEFAULT_ARGS, BrowserProfile


def _default_args_in_order(profile: BrowserProfile) -> list[str]:
	args = profile.get_args()
	arg_set = set(args)
	return [arg for arg in CHROME_DEFAULT_ARGS if arg in arg_set]


def test_get_args_preserves_default_order_with_ignore_list() -> None:
	profile = BrowserProfile(
		ignore_default_args=['--disable-popup-blocking'],
		user_data_dir='/tmp/browser-use-test-profile',
		enable_default_extensions=False,
	)

	args = profile.get_args()

	assert '--disable-popup-blocking' not in args
	expected = [arg for arg in CHROME_DEFAULT_ARGS if arg not in set(profile.ignore_default_args)]
	assert _default_args_in_order(profile) == expected


def test_get_args_returns_all_defaults_in_order_without_ignore() -> None:
	profile = BrowserProfile(
		ignore_default_args=[],
		user_data_dir='/tmp/browser-use-test-profile',
		enable_default_extensions=False,
	)

	assert _default_args_in_order(profile) == CHROME_DEFAULT_ARGS


def test_get_args_ignores_all_defaults_when_true() -> None:
	profile = BrowserProfile(
		ignore_default_args=True,
		user_data_dir='/tmp/browser-use-test-profile',
		enable_default_extensions=False,
	)

	args = profile.get_args()

	assert not any(arg in args for arg in CHROME_DEFAULT_ARGS)
