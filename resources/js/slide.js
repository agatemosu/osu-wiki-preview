// @ts-check

/**
 * @param {HTMLElement} element
 * @param {number} duration
 */
export function slideDown(element, duration) {
	element.style.display = "block";
	element.style.overflow = "hidden";
	const totalHeight = element.scrollHeight;
	let startTime;

	/**
	 * @param {number} time
	 */
	const animate = (time) => {
		if (!startTime) {
			startTime = time;
		}

		const elapsed = time - startTime;
		const progress = elapsed / duration;
		element.style.height = `${totalHeight * progress}px`;

		if (progress < 1) {
			requestAnimationFrame(animate);
		} else {
			element.removeAttribute("style");
			element.style.display = "block";
		}
	};

	requestAnimationFrame(animate);
}

/**
 * @param {HTMLElement} element
 * @param {number} duration
 */
export function slideUp(element, duration) {
	const totalHeight = element.scrollHeight;
	let startTime;

	/**
	 * @param {number} time
	 */
	const animate = (time) => {
		if (!startTime) {
			startTime = time;
		}

		const elapsed = time - startTime;
		const progress = elapsed / duration;
		element.style.height = `${totalHeight * (1 - progress)}px`;

		if (progress < 1) {
			requestAnimationFrame(animate);
		} else {
			element.removeAttribute("style");
			element.style.display = "none";
		}
	};

	element.style.overflow = "hidden";
	requestAnimationFrame(animate);
}
