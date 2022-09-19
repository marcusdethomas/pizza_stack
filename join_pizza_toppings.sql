SELECT * FROM pizza inner join pizza_has_topping on pizza.id = pizza_has_topping.pizza_id
inner join topping on topping.id = topping_id 
where pizza.id = pizza.id