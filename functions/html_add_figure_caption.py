from bs4 import BeautifulSoup


def add_figure_caption(html):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Find all img elements with the title attribute within a <p> element
    img_elements = soup.select("p img[title]")

    # Iterate through each found img element
    for img_element in img_elements:
        # Get the value of the title attribute
        title_text = img_element["title"]

        # Create a new <em> element with the hardcoded class and the text from the title attribute
        em_element = soup.new_tag("em", attrs={"class": "osu-md__figure-caption"})
        em_element.string = title_text

        # Insert the <em> element after the <img> element
        img_element.insert_after(em_element)

    # Get the modified HTML code
    modified_html = str(soup)

    return modified_html
