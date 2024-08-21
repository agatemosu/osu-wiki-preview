function slide(
	element: HTMLElement,
	options: KeyframeAnimationOptions,
	onFinish?: () => void,
) {
	element.style.display = "block";
	const totalHeight = element.scrollHeight;

	const keyframes: Keyframe[] = [
		{ height: "0px", opacity: 0, overflow: "hidden" },
		{ height: `${totalHeight}px`, opacity: 1, overflow: "hidden" },
	];

	const animation = element.animate(keyframes, options);

	animation.onfinish = () => {
		if (onFinish) onFinish();
	};
}

type SlideAction = (
	element: HTMLElement,
	duration: number,
	onFinish?: () => void,
) => void;

export const slideDown: SlideAction = (element, duration, onFinish) => {
	const options: KeyframeAnimationOptions = {
		direction: "normal",
		duration: duration,
	};

	slide(element, options, onFinish);
};

export const slideUp: SlideAction = (element, duration, onFinish) => {
	const options: KeyframeAnimationOptions = {
		direction: "reverse",
		duration: duration,
	};

	slide(element, options, onFinish);
};
