import { fadeToggle } from "@/utils/fade.ts";

const elements = new Set();

export function blackoutToggle(element: any, state: boolean) {
	if (state) {
		elements.add(element);
	} else {
		elements.delete(element);
	}

	fadeToggle(document.body.querySelector(".js-blackout"), blackoutVisible());
}

export function blackoutVisible() {
	return elements.size > 0;
}
