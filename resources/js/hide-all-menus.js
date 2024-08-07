// @ts-check

import { fadeOut } from "./fade.js";
import { setButtonInactive, setMenuInactive } from "./menus.js";
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
		setMenuInactive(menu);
	}

	const activeButtons = $$(".js-click-menu--active[data-click-menu-target]");
	for (const button of activeButtons) {
		setButtonInactive(button);
	}

	const activeBlackout = $('.js-blackout[data-visibility="visible"]');
	if (activeBlackout) {
		fadeOut(activeBlackout);
	}

	document.body.classList.remove("js-nav2--active");
}
