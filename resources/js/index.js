// @ts-check

import "../css/app.less";
import { hideAllMenus } from "./hide-all-menus.js";
import { setupMenus, setupMobileMenus } from "./setup-menus.js";
import { setupTooltips } from "./setup-tooltips.js";

setupMenus();
setupMobileMenus();
setupTooltips();

document.addEventListener("click", onClick);
document.addEventListener("scroll", onScroll);

/**
 * @param {MouseEvent} event
 */
function onClick(event) {
	hideAllMenus(event);
}

function onScroll() {
	document.body.classList.toggle("js-header-is-pinned", window.scrollY > 30);
}
