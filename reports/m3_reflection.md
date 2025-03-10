# Milestone 3 Reflection

Milestone Contributors: Mu (Henry) Ha, Javier Martinez, Stephanie Ta, and Zuer (Rebecca) Zhong

## Implemented Parts of the Proposal and Sketch

**Optimized Ingredient Visualization:**
The original design displayed all ingredients in a bar chart, requiring users to scroll, which was cumbersome. We now limit the chart to the top ten ingredients, ensuring immediate clarity. A complete list of additional ingredients is provided separately, aligning with Daniel’s suggestion. This change effectively reduces visual clutter without sacrificing data completeness.

**Enhanced Recipe Data Presentation:**
We introduced detailed tooltips that now include a rounded ingredient quantity (to one decimal place), unit, and ingredient name. Additionally, the recipe count, previously a separate element, has been integrated into the recipe list block. This integration streamlines the display and creates a more cohesive user experience.

**Improved Interaction and Navigation:**
Icons for categories and subcategories have been added, making navigation more intuitive. A “deselect all” button for filters was implemented to allow users to quickly reset their selections, further simplifying interaction.

**Visual and Layout Updates:**
The dashboard now features a new, cohesive color scheme that fits the cookies theme, making it visually appealing and consistent. The title has been made more prominent with a larger font, and figure sizes have been made more dynamic to better utilize available space across different screen sizes. Similar and related components are now placed closer together, making the overall layout more intuitive.

## Non-Implemented Parts of the Proposal and Sketch

**Component Cards:**
Although we initially explored encapsulating figure components into cards as suggested by Daniel, the dynamic resizing challenges led us to maintain the original component layout. This decision was based on the need for a reliable and responsive design over the potential aesthetic improvements offered by card components. However, this lead to a lot of complications (such as figure sizes not changing despite trying a lot of ways to make them dynamic in a card), so we decided to keep the components as they are instead of turning them into cards.

**Corner Cases and Responsiveness:**
While the majority of features function as expected, we acknowledge that some corner cases, such as minor responsiveness issues on specific screen sizes, still need further refinement. We plan on implementing this in the future.

## Things Done Differently than in the Proposal and Sketch
We deviated from the original white-background sketch in several ways to create a more thematic and user-friendly dashboard. First, we adopted a cookie-themed brown palette rather than a neutral color scheme, adding distinct shaded panels to group related components and reinforce the subject matter. We limited the ingredient chart to display only the top ten ingredients (with a separate comprehensive list), preventing scrolling and reducing visual clutter. The dashboard title evolved from a generic label to “Cookie Dash,” complete with a cookie icon, and we introduced icons for key categories (e.g., flour, sweetener, fat) to make filtering more intuitive. Rather than keeping the recipe count and complexity separate, we combined them into a single “Recipes & Complexity” panel, streamlining information display. We also enhanced tooltips to include rounded ingredient quantities, units, and names, adding depth to the recipe data presentation. In contrast to the original concept of static cards, we avoided card components altogether due to challenges with dynamic resizing and responsiveness, opting instead for flexible panels. Finally, to simplify user interaction, we added a “Deselect All” filter button and replaced the plain numeric average rating with a circular gauge, thus improving both functionality and visual appeal.

## Potential Future Improvements and Additions

At the moment, our dashboard does a good job at displaying overall information about recipes that match the filters that are available. In the future, we would also like to improve the format of the dashboard, so that the dashboard displays nicely for all screen sizes.

## Intentional Deviations from Visualization Best Practices

We have not intentionally deviated from any of the best practices that we learned in 531 regarding effective visualizations.

## Challenging

I added tooltips to our dashboard as inspiration from Group 4, who effectively use tooltips on their plots. Their implementation enhances data accessibility and interactivity. By integrating similar tooltips into our dashboard, users can view rounded ingredient quantities, units, and names without cluttering the visual space. This approach not only improves interactivity but also avoids complexity.
