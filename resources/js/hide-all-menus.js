// @ts-check

import { $, $$ } from "./utils.js";

/**
 * @param {MouseEvent} event
 */
export function hideAllMenus(event) {
	if (!event.target) {
		return;
	}

	const targetElement = /** @type {Element} */ (event.target);

	const isClickInsideMenu = targetElement.closest("[data-click-menu-id]");
	if (isClickInsideMenu) {
		return;
	}

	const visibleMenus = $$('.js-click-menu--active[data-visibility="visible"]');
	for (const menu of visibleMenus) {
		menu.dataset.visibility = "hidden";
		menu.classList.remove("js-click-menu--active");
	}

	const activeButtons = $$(".js-click-menu--active[data-click-menu-target]");
	for (const button of activeButtons) {
		button.classList.remove("js-click-menu--active");
	}

	const activeBlackout = $('.js-blackout[data-visibility="visible"]');
	if (activeBlackout) {
		activeBlackout.dataset.visibility = "hidden";
	}

	document.body.classList.remove("js-nav2--active");
}
