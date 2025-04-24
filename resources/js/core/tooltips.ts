import { DateTime } from "luxon";
import tippy from "tippy.js";

export class Tooltips {
	constructor() {
		const timeElements = document.querySelectorAll("time");

		for (const el of timeElements) {
			el.title = this.timeagoTip(el, el.title).outerHTML;
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
				delay: 100,
				duration: 200,
			});
			el.removeAttribute("title");
		}
	}

	timeagoTip = (el: HTMLTimeElement, title: string) => {
		const timeString = el.dateTime ?? title;
		const time = DateTime.fromISO(timeString);

		const $dateEl = document.createElement("strong");
		$dateEl.textContent = time.toLocaleString(DateTime.DATE_FULL);

		const $timeEl = document.createElement("span");
		$timeEl.classList.add("tippy-box__time");
		$timeEl.textContent = `${time.toLocaleString(DateTime.TIME_WITH_SECONDS)} ${time.offsetNameShort}`;

		const $tipEl = document.createElement("span");
		$tipEl.append($dateEl);
		$tipEl.append(" ");
		$tipEl.append($timeEl);

		return $tipEl;
	};
}
