// @ts-check

/**
 * @param {HTMLElement} el
 */
export function isVisible(el) {
	return el.dataset.visibility !== "hidden";
}

/**
 * @param {HTMLElement} el
 */
export function fadeIn(el) {
	el.dataset.visibility = "visible";
}

/**
 * @param {HTMLElement} el
 */
export function fadeOut(el) {
	el.dataset.visibility = "hidden";
}

/**
 * @param {HTMLElement} el
 * @param {boolean?} makeVisible
 */
export function fadeToggle(el, makeVisible) {
	const fn = makeVisible ?? !isVisible(el) ? fadeIn : fadeOut;

	fn(el);
}
