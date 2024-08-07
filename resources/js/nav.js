// @ts-check

import { fadeIn, fadeOut, isVisible } from "./fade.js";
import { openClickMenu } from "./menus.js";
import { $, $$ } from "./utils.js";

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
	if (isMenuVisible) {
		clickMenuTarget.style.display = "none";

		document.body.classList.remove("js-nav2--active");
		fadeOut(blackoutElement);

		closeAllTabs();
		return;
	}

	openDefaultTab();

	// In osu-web, it has an animation
	clickMenuTarget.style.display = "block";

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
