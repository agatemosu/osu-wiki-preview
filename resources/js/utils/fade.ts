function isVisible(el: HTMLElement) {
	return el.dataset.visibility !== "hidden";
}

export function fadeIn(el: HTMLElement) {
	el.dataset.visibility = "visible";
}

export function fadeOut(el: HTMLElement) {
	el.dataset.visibility = "hidden";
}

export function fadeToggle(el: HTMLElement | null, makeVisible?: boolean) {
	if (el == null) return;

	const fn = makeVisible ?? !isVisible(el) ? fadeIn : fadeOut;

	fn(el);
}
