Bicycle Shop

You're tasked with building a website that allows Marcus, a bicycle shop owner, to sell his bicycles.

Marcus owns a growing business and now wants to sell via the internet. He also tells you that bicycles are his main product, but if the business continues to grow, he will surely start selling other sports-related items such as skis, surfboards, roller skates, etc. It would be a nice bonus if the same website allowed him to sell those things as well.

What makes Marcus's business successful is that customers can completely customize their bicycles. They can select many different options for the various parts of the bicycle. Here is an incomplete list of all the parts and their possible choices, to give an example:

Parts Type: Frame type, Frame finish, Wheels, Rim color, Chain

Frame type: Full-suspension, diamond, step-through
Frame finish: Matte, shiny
Wheels: Road wheels, mountain wheels, fat bike wheels
Rim color: Red, black, blue
Chain: Single-speed chain, 8-speed chain

On top of that, Marcus points out that there are some combinations that are prohibited because they are not possible in reality. For example:

If you select "mountain wheels", then the only frame available is the full suspension.
If you select "fat bike wheels", then the red rim color is unavailable because the manufacturer doesn't provide it.

Also, sometimes Marcus doesn't have all the possible variations of each part in stock, so he also wants to be able to mark them as "temporarily out of stock" to avoid incoming orders that he would not be able to fulfill.

We ask you to provide a working web application that covers the needs that Marcus has. The minimum parts that we expect to be covered are:

The public part of this minimal e-commerce website:

- A page that displays the list of bicycles that are on sale
- A page that displays one bicycle in particular, where the customer can choose the different options for customization. This page should have an “Add to cart” button, that when clicked will persist the selected bicycle into the user’s cart.
- My cart page, where the user can see the bicycles he already configured when clicked on “Add to cart”. The user shouldn’t be able to add to cart with a forbidden combination of options or out of stock parts.

The private part of the site, where Marcus can configure the bicycles:

Marcus should be able to create and delete bicycles
Marcus should be able manage what parts are offered on each bicycle: Configure what characteristic are available of any given bicycle (rim color, wheels, etc.) and what options inside those characteristics are offered (ex: the rim color for this bike can be red, blue or black, etc.).

There’s no need to implement authentication, a checkout process or a nice design, you can just focus on the functionality described.

You can choose the tech stack that you prefer, and you can use any third party tool or library that you want. For any other specification of the system that's not directly stated in the exercise, feel free to interpret it as you see best.
