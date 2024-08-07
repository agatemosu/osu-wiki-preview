// @ts-check

import tippy from "tippy.js";
import { $$ } from "./utils/selectors.js";

export function setupTooltips() {
	const elements = $$("[title]");

	for (const el of elements) {
		if (!el.title) {
			continue;
		}

		tippy(el, {
			content: el.title,
			theme: "osu",
			delay: 100,
			duration: 200,
		});
		el.removeAttribute("title");
	}
}
