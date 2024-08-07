// @ts-check

import { openClickMenu } from "./menus.js";
import { fadeIn, fadeOut, isVisible } from "./utils/fade.js";
import { $, $$ } from "./utils/selectors.js";
import { slideDown, slideUp } from "./utils/slide.js";

let activeNavTimeout;
const blackoutElement = /** @type {HTMLElement} */ ($(".js-blackout"));

function closeAllTabs() {
	const allButtons = $$(".mobile-menu-tab[data-click-menu-target]");
	for (const button of allButtons) {
		button.classList.remove("js-click-menu--active");
	}

	const allTabs = $$(".mobile-menu__item[data-click-menu-id]");
	for (const tab of allTabs) {
		tab.classList.remove("js-click-menu--active");
		fadeOut(tab);
	}
}

function openDefaultTab() {
	const clickMenuId = "mobile-nav";
	const tab = $(`[data-click-menu-target="${clickMenuId}"]`);
	const clickMenuTarget = $(`[data-click-menu-id="${clickMenuId}"]`);

	if (!tab || !clickMenuTarget) {
		return;
	}

	openClickMenu(tab, clickMenuTarget);
}

/**
 * @param {HTMLElement} clickMenuTarget
 * @param {boolean} isMenuVisible
 */
export function toggleNav(clickMenuTarget, isMenuVisible) {
	const duration = 150;

	if (isMenuVisible) {
		fadeOut(blackoutElement);

		slideUp(clickMenuTarget, duration);
		closeAllTabs();

		activeNavTimeout = setTimeout(() => {
			document.body.classList.remove("js-nav2--active");
		}, duration);
		return;
	}

	clearTimeout(activeNavTimeout);

	openDefaultTab();
	slideDown(clickMenuTarget, duration);

	document.body.classList.add("js-nav2--active");
	fadeIn(blackoutElement);
}

/**
 * @param {HTMLElement} button
 * @param {HTMLElement} clickMenuTarget
 */
export function toggleNavTab(button, clickMenuTarget) {
	const isTabActive = isVisible(clickMenuTarget);

	closeAllTabs();

	if (isTabActive) {
		openDefaultTab();
		return;
	}

	openClickMenu(button, clickMenuTarget);
}
