# Milestone 4 Reflection

Milestone Contributors: Mu (Henry) Ha, Javier Martinez, Stephanie Ta, and Zuer (Rebecca) Zhong

## Implemented/Refined Parts of the Proposal and Sketch

According to Daniel’s and peers’ suggestions, we enhanced the filters by implementing several improvements: we pre-selected a subcategory to streamline the user experience and improve usability. Additionally, we sorted the ingredients based on their popularity score to prioritize relevant options. Lastly, we refined the UI by rounding the popularity score to two decimal digits, providing a cleaner and more visually consistent interface. These changes contributed significantly to a more intuitive and user-friendly experience.

Embracing Daniel’s feedback on sorting the ingredients, we also sorted the recipe list by recipe index. Additionally, we aligned the complexity score to the right to enhance visual alignment and consistency. Based on our classmate's recommendation, we updated the tooltip to provide clearer guidance. This iterative refinement has improved both usability and the overall interface experience.

## Differences from Original Proposal/Sketch

We found the feedback on readability particularly useful. Initially, the additional ingredients list was difficult to read because of its small font size and lack of scrolling functionality. Since Milestone 3, we increased the font size and made the list scrollable, improving usability and accommodating longer ingredient lists. Although our initial proposal suggested a different layout, we adjusted it based on usability testing, resulting in a more balanced and user-friendly interface.

## Technical Enhancements

To increase our app’s performance, we stored processed data in a binary Parquet file for faster reading and implemented caching via `flask_caching`. As our app was already quite responsive, Daniel indicated there was no need to overly optimize redundant filtering or computations.

Additionally, we refined the layout to ensure that the entire dashboard now fits on a single page.

## Addressed Peer Feedback

All peer feedback that we have addressed can be found here: [GitHub Issue #77](https://github.com/UBC-MDS/DSCI-532_2025_1_cookie-dash/issues/77).

## Intentional Deviations from Visualization Best Practices

We have not intentionally deviated from any visualization best practices learned in DSCI 531.

## Dashboard Strengths and Limitations

Currently, our dashboard provides clear visualizations and intuitive interactivity. It effectively prioritizes information through sorted filters, readable ingredient lists, and refined tooltips. However, we acknowledge that the layout may still have minor responsiveness issues on very specific screen sizes. This is a limitation we plan to address in future iterations.

## Potential Future Improvements

With additional time, we would enhance dashboard responsiveness to ensure seamless functionality across all screen sizes. We also envision adding more detailed analytics or interactive features, such as user-driven comparisons between recipes or dynamic ingredient substitution suggestions, to further enrich user experience.

## Particularly Useful Insights and Desired Support

Feedback emphasizing readability and UI consistency proved particularly valuable, directly improving user engagement and interface clarity. Additionally, having a clearer file structure presented in the first lab would have been beneficial, as we initially had each component in separate .py files and later needed to reorganize them into callback.py and component.py. If anything, more structured guidance or demonstrations on dynamic component resizing would have helped overcome earlier implementation challenges.
