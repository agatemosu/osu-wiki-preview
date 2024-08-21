import dayjs from "dayjs";
import tippy from "tippy.js";

export class Tooltips {
	constructor() {
		const timeElements = document.querySelectorAll("time");

		for (const el of timeElements) {
			const datetime = dayjs(el.dateTime);

			const date = datetime.format("D MMMM YYYY");
			const time = datetime.format("HH:mm:ss");
			const offset = datetime.format("[UTC]Z");

			const dateEl = document.createElement("b");
			dateEl.textContent = date;

			const textEl = document.createElement("span");
			textEl.style.color = "hsl(var(--hsl-l2))";
			textEl.textContent = `${time} ${offset}`;

			el.title = `${dateEl.outerHTML} ${textEl.outerHTML}`;
		}

		const elements = document.querySelectorAll("[title]");

		for (const el of elements) {
			if (!(el instanceof HTMLElement)) {
				continue;
			}

			if (el.title === "") {
				continue;
			}

			tippy(el, {
				content: el.title,
				allowHTML: true,
				theme: "osu",
				delay: 100,
				duration: 200,
			});
			el.removeAttribute("title");
		}
	}
}
