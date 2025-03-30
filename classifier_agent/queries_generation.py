import csv


# Define queries with categories
queries = [
    # General Health
    ("Sometimes I wake up feeling shaky—how do I know if it’s my blood sugar or just anxiety?", "General Health"),
    ("Is there a difference between being tired from high blood sugar and just regular exhaustion?", "General Health"),
    ("Why do I feel dizzy after eating a meal, even if my glucose levels seem okay?", "General Health"),
    ("Can stress cause my blood sugar to drop, or is it just in my head?", "General Health"),
    ("I keep getting headaches after meals—could it be my diabetes, dehydration, or something else?", "General Health"),
    ("What are the long-term effects of occasional high blood sugar spikes if I usually manage well?", "General Health"),
    ("How can I tell if my frequent thirst is from diabetes or if I just don’t drink enough water?", "General Health"),
    ("Are gut health and blood sugar connected? My digestion feels off lately.", "General Health"),
    ("Is interrupted sleep more likely from blood sugar fluctuations or general insomnia?", "General Health"),
    ("How do I distinguish between diabetic neuropathy and normal muscle pain after exercise?", "General Health"),
    ("Why do I feel so weak and shaky when my blood sugar is low, even if it’s not that low?", "General Health"),
    ("How can I manage my blood sugar levels throughout the day?", "general_health"),
    ("What are the signs of high blood sugar (hyperglycemia), and how should I handle it?", "general_health"),
    ("What are the symptoms of low blood sugar (hypoglycemia), and what should I do?", "general_health"),
    ("How does sleep affect my blood sugar levels?", "general_health"),
    ("How much water should I drink daily to stay hydrated and manage my diabetes?", "general_health"),
    ("Is thin-crust pizza better than regular pizza for blood sugar control?", "food/nutrition"),
    ("Does adding protein to my pizza meal help with glucose control?", "food/nutrition"),
    ("Is cauliflower crust pizza a better option for Type 1 Diabetes?", "food/nutrition"),
      ("Why am I always so thirsty even when my sugar is normal?", "general_health"),
    ("I feel tired even when my blood sugar is in range. What’s wrong?", "general_health"),
    ("Why do my legs feel tingly when I sit for too long?", "general_health"),
    ("Does diabetes make my immune system weaker?", "general_health"),
    ("Why do I get headaches when my blood sugar is normal?", "general_health"),
    ("Is it normal to feel dizzy when my blood sugar is dropping?", "general_health"),
    ("Why do I bruise so easily after insulin injections?", "general_health"),
    ("Can stress make my blood sugar spike even if I don’t eat anything?", "general_health"),
    ("Why do my feet feel cold even when it's warm?", "general_health"),
    ("I keep getting infections. Does diabetes make it worse?", "general_health"),
    ("How do I know if I have nerve damage from diabetes?", "general_health"),
    ("Why do my blood sugars go up when I’m sick?", "general_health"),
    ("Does dehydration affect blood sugar levels?", "general_health"),
    ("Why does my vision get blurry when my blood sugar is high?", "general_health"),
    ("I always feel bloated after eating carbs. Is that normal?", "general_health"),
    ("Why do I wake up with high blood sugar even when I eat low-carb at night?", "general_health"),
    ("Is it safe to take painkillers like ibuprofen with diabetes?", "general_health"),
    ("Why does my blood sugar go up after workouts instead of down?", "general_health"),
    ("Does diabetes make sleep problems worse?", "general_health"),
    ("How do I deal with fatigue from fluctuating blood sugar?", "general_health"),("I'm so sick of carb counting—it’s exhausting.", "mental_health"),
    ("Why does diabetes make me feel so anxious all the time?", "mental_health"),
    ("I feel guilty every time I eat something high-carb.", "mental_health"),
    ("It's frustrating when people tell me what I should or shouldn’t eat.", "mental_health"),
    ("I hate having to think about food constantly—it's overwhelming.", "mental_health"),
    ("I get really stressed out when my blood sugar goes too high or low.", "mental_health"),
    ("Why do I feel so irritable when my blood sugar drops?", "mental_health"),
    ("I feel like diabetes controls my whole life. Is that normal?", "mental_health"),
    ("I wish I could just eat like my friends without worrying.", "mental_health"),
    ("Does diabetes make depression worse? I feel down a lot.", "mental_health"),
    ("I overeat when I’m stressed—how do I stop?", "mental_health"),
    ("I feel so alone dealing with diabetes—no one gets it.", "mental_health"),
    ("Every time my sugar spikes, I feel like a failure.", "mental_health"),
    ("I feel judged when I eat sweets in public. How do I deal with that?", "mental_health"),
    ("I get super anxious before doctor visits. What if my A1C is bad?", "mental_health"),
    ("People think I got diabetes from eating too much sugar, and it annoys me.", "mental_health"),
    ("I have diabetes burnout—I just want to stop managing it for a while.", "mental_health"),
    ("I feel like I’m constantly explaining myself. It’s exhausting.", "mental_health"),
    ("I get nervous eating at restaurants because I don’t know the carb counts.", "mental_health"),
    ("Does diabetes make it harder to handle emotions, or is it just me?", "mental_health"),
     ("I'm so exhausted from all this", "mental_health"),
      ("I’m craving pizza tonight—will it totally mess up my blood sugar?", "food/nutrition"),
    ("Do blood sugar spikes always happen after eating pizza, or am I doing something wrong?", "food/nutrition"),
    ("Is deep-dish pizza a worse choice than thin-crust for managing diabetes?", "food/nutrition"),
    ("Any tips on enjoying pizza without completely throwing off my glucose levels?", "food/nutrition"),
    ("Would eating a side salad with pizza help keep my blood sugar stable?", "food/nutrition"),
    ("If I take extra insulin, can I eat pizza without worrying about spikes?", "food/nutrition"),
    ("Someone told me cold pizza has a lower glycemic impact—is that true?", "food/nutrition"),
    ("Would it be better to have pizza earlier in the day instead of for dinner?", "food/nutrition"),
    ("How much worse is stuffed-crust pizza compared to a regular slice for T1D?", "food/nutrition"),
    ("Should I completely avoid pizza, or is portion control the key?", "food/nutrition"),
    ("Are there any fast-food burgers that won’t send my blood sugar through the roof?", "food/nutrition"),
    ("If I eat fries with protein, will that help reduce a glucose spike?", "food/nutrition"),
    ("Is switching to brown rice sushi actually better for blood sugar control?", "food/nutrition"),
    ("Carb counting is exhausting—what happens if I just guess instead?", "food/nutrition"),
    ("Are sugar-free sodas really a safe choice, or do they still affect my blood sugar?", "food/nutrition"),
    ("Does eating protein with carbs actually help smooth out sugar spikes?", "food/nutrition"),
    ("What’s the best dessert option if I want something sweet but don’t want a sugar crash?", "food/nutrition"),
    ("If I eat a donut for breakfast, will my blood sugar stay high all day?", "food/nutrition"),
    ("How can I enjoy street food without completely messing up my glucose control?", "food/nutrition"),
    ("If I have to choose, is it better to skip a meal or eat something unhealthy?", "food/nutrition"),

  
    ("Are French fries worse than mashed potatoes for blood sugar?", "food/nutrition"),
    ("Does eating fried chicken affect my blood sugar differently than grilled?", "food/nutrition"),
    ("Is it better to eat a burger with or without the bun for Type 1 Diabetes?", "food/nutrition"),
    ("What are the best fast food options for stable blood sugar?", "food/nutrition"),
    ("Is brown rice sushi better than white rice sushi for diabetes?", "food/nutrition"),
    ("What’s a good alternative to pasta if I crave Italian food?", "food/nutrition"),


    ("Are sugar-free desserts really safe for diabetics?", "food/nutrition"),
    ("Is dark chocolate a good snack for Type 1 Diabetes?", "food/nutrition"),
    ("Do sugar-free candies actually help in managing diabetes?", "food/nutrition"),
    ("Should I choose fruit over dessert for a post-dinner treat?", "food/nutrition"),
    ("Is honey a better alternative to sugar for a Type 1 Diabetic?", "food/nutrition"),


    ("How many carbs are in a bowl of poha?", "food/nutrition"),
    ("Is masala dosa higher in carbs than plain dosa?", "food/nutrition"),
    ("What’s the fiber content in rajma and how does it help blood sugar?", "food/nutrition"),
    ("How do I estimate carbs in a homemade chapati?", "food/nutrition"),
    ("Do rotis made with multigrain flour have fewer carbs than wheat rotis?", "food/nutrition"),

    # Glycemic Index & Blood Sugar Impact
    ("Is the glycemic index of basmati rice lower than regular rice?", "food/nutrition"),
    ("Which has a lower glycemic load: dal or sambar?", "food/nutrition"),
    ("Are bananas too high in sugar for Type 1 Diabetics?", "food/nutrition"),
    ("Does adding ghee to rice lower its glycemic index?", "food/nutrition"),
    ("Which fruits are safest for stable blood sugar levels?", "food/nutrition"),

    # Drinks & Hydration
    ("Does black coffee without sugar affect blood sugar levels?", "food/nutrition"),
    ("Are fruit juices safe if I have Type 1 Diabetes?", "food/nutrition"),
    ("Which milk alternatives (almond, soy, oat) have the fewest carbs?", "food/nutrition"),
    ("How many carbs are in a glass of buttermilk?", "food/nutrition"),
    ("Is coconut water a good drink for T1D?", "food/nutrition"),

    # Food Combinations & Meal Timing
    ("Does eating protein with carbs reduce blood sugar spikes?", "food/nutrition"),
    ("Is it better to eat a protein-rich breakfast to prevent morning sugar spikes?", "food/nutrition"),
    ("Can I replace rice with quinoa for better blood sugar control?", "food/nutrition"),
    ("What are good low-carb snacks for school or work?", "food/nutrition"),
    ("Which dal has the lowest carbs: moong, toor, or masoor?", "food/nutrition"),

  
    # Menstrual Cycle & Hormones
    ("How does my menstrual cycle affect my blood sugar levels?", "general_health"),
    ("Why do I experience high blood sugars before my period?", "general_health"),
    ("How can I adjust my insulin around my menstrual cycle?", "general_health"),
    ("Does birth control affect blood sugar levels?", "general_health"),
    ("How does menopause impact Type 1 Diabetes management?", "general_health"),

    # General general's Health & Diabetes
    ("How does stress impact my blood sugar as a woman?", "general_health"),
    ("Are general with Type 1 Diabetes at higher risk for yeast infections?", "general_health"),
    ("Does T1D increase the risk of osteoporosis in general?", "general_health"),
    ("What are the best ways to manage weight with Type 1 Diabetes?", "general_health"),
    ("How does breastfeeding impact blood sugar levels?", "general_health"),
    ("Can my blood sugar changes cause mood swings?", "general_health"),
    ("Why do I have insulin resistance during certain times of my cycle?", "general_health"),
    ("Are women with T1D more likely to have thyroid issues?", "general_health"),
    ("How can I manage cravings and blood sugar fluctuations during PMS?", "general_health"),
    ("What are the best exercises for general with Type 1 Diabetes?", "general_health"),


    # Exercise & Physical Activity
    ("How does exercise impact my blood sugar levels?", "general_health"),
    ("Should I check my blood sugar before and after workouts?", "general_health"),
    ("What types of exercise are best for managing Type 1 Diabetes?", "general_health"),
    ("How can I prevent blood sugar crashes during or after exercise?", "general_health"),
    ("Is it safe to exercise if my blood sugar is above or below a certain level?", "general_health"),

    # Illness & Immune Health
    ("What should I do if I feel sick and my blood sugar is high?", "general_health"),
    ("How does having a cold or flu affect my insulin needs?", "general_health"),
    ("How can I strengthen my immune system with Type 1 Diabetes?", "general_health"),
    ("Are there specific vaccines or precautions I should take as a person with T1D?", "general_health"),
    ("How do I know if I’m experiencing diabetic ketoacidosis (DKA), and what should I do?", "general_health"),

    # Medication & Insulin Management
    ("How often should I change my insulin pump site?", "general_health"),
    ("What happens if I accidentally take too much or too little insulin?", "general_health"),
    ("How do I properly store insulin to keep it effective?", "general_health"),
    ("How can I manage dawn phenomenon (high blood sugar in the morning)?", "general_health"),
    ("What should I do if my continuous glucose monitor (CGM) readings seem inaccurate?", "general_health"),
     ("How should I adjust my insulin dosage if my blood sugar is 250 mg/dL before a meal?", "General Health"),
    ("What are quick ways to treat hypoglycemia if my blood sugar drops below 70 mg/dL?", "General Health"),
    ("Can stress affect my blood sugar levels, and how do I manage this?", "General Health"),
    ("How might my menstrual cycle affect my insulin sensitivity this week?", "General Health"),
    ("What foods can I eat that won't spike my blood sugar but will still give me energy for exercise?", "General Health"),
    ("How should I adjust my basal insulin during my period when my blood sugars tend to run higher?", "General Health"),
    ("What should I do if my continuous glucose monitor shows a rapid drop in blood sugar while I'm sleeping?", "General Health"),
    ("Is it safe for me to fast for 16 hours with Type 1 diabetes?", "General Health"),
    ("How do I calculate my insulin-to-carb ratio for a high-protein, low-carb meal?", "General Health"),
    ("What are the signs that I need to change my insulin pump site?", "General Health"),
    ("How can I prevent skin irritation at my CGM and pump sites during my period when my skin is more sensitive?", "General Health"),
    ("What should I do if I'm sick with the flu and can't keep food down but need to manage my blood sugar?", "General Health"),
    ("How much should I reduce my insulin before a 30-minute cardio workout?", "General Health"),
    ("Why might I experience dawn phenomenon where my blood sugar rises early in the morning?", "General Health"),
    ("How can I manage my diabetes during menstruation when my blood sugar levels are more unpredictable?", "General Health"),
     # Insulin Pump & CGM Issues
    ("Why is my insulin pump site suddenly painful or red?", "pump_cgm"),
    ("What should I do if my insulin pump cannula is bent or kinked?", "pump_cgm"),
    ("Why am I getting unexpected high blood sugars despite changing my pump site?", "pump_cgm"),
    ("How often should I change my insulin pump infusion set?", "pump_cgm"),
    ("What should I do if my insulin pump stops delivering insulin?", "pump_cgm"),
    ("Why does my CGM show different readings compared to my fingerstick test?", "pump_cgm"),
    ("What should I do if my CGM sensor falls off before it’s supposed to?", "pump_cgm"),
    ("Why is my CGM giving me 'sensor error' or 'no readings'?", "pump_cgm"),
    ("How can I prevent my CGM sensor from coming loose due to sweat or exercise?", "pump_cgm"),
    ("Why is my CGM reading delayed compared to my actual blood sugar?", "pump_cgm"),
    ("How do I know if my insulin pump is leaking or not delivering properly?", "pump_cgm"),
    ("What should I do if my insulin gets too warm or cold in my pump?", "pump_cgm"),
    ("Can I go through airport security with my insulin pump and CGM?", "pump_cgm"),
    ("How do I handle insulin pump failures when I’m traveling or away from home?", "pump_cgm"),
    ("Why does my CGM show constant highs or lows that don’t match how I feel?", "pump_cgm"),
    ("Should I calibrate my CGM, and if so, how often?", "pump_cgm"),
    ("What should I do if my pump or CGM malfunctions at night while I’m asleep?", "pump_cgm"),
    ("Why does my CGM sensor sometimes take longer to warm up and give readings?", "pump_cgm"),
    ("What backup supplies should I always carry in case my pump or CGM fails?", "pump_cgm"),
     ("Is thin-crust pizza better than regular pizza for blood sugar control?", "food/nutrition"),
    ("Does adding protein to my pizza meal help with glucose control?", "food/nutrition"),
    ("Is cauliflower crust pizza a better option for Type 1 Diabetes?", "food/nutrition"),

    # 🍟 Fast Food & Takeout
    ("Are French fries worse than mashed potatoes for blood sugar?", "food/nutrition"),
    ("Does eating fried chicken affect my blood sugar differently than grilled?", "food/nutrition"),
    ("Is it better to eat a burger with or without the bun for Type 1 Diabetes?", "food/nutrition"),
    ("What are the best fast food options for stable blood sugar?", "food/nutrition"),
    ("Is brown rice sushi better than white rice sushi for diabetes?", "food/nutrition"),
    ("What’s a good alternative to pasta if I crave Italian food?", "food/nutrition"),

    # 🍩 Desserts & Sweet Cravings
    ("Are sugar-free desserts really safe for diabetics?", "food/nutrition"),
    ("Is dark chocolate a good snack for Type 1 Diabetes?", "food/nutrition"),
    ("Do sugar-free candies actually help in managing diabetes?", "food/nutrition"),
    ("Should I choose fruit over dessert for a post-dinner treat?", "food/nutrition"),
    ("Is honey a better alternative to sugar for a Type 1 Diabetic?", "food/nutrition"),

    
   
    
    
    # Mental Health
    ("How do I know if my mood swings are due to my blood sugar or just normal emotions?", "Mental Health"),
    ("Why does managing my diabetes sometimes feel more exhausting than the condition itself?", "Mental Health"),
    ("Can blood sugar fluctuations trigger panic attacks, or am I just imagining a connection?", "Mental Health"),
    ("How do I stop feeling guilty every time my A1C isn’t perfect?", "Mental Health"),
    ("Is diabetes burnout a real thing, or am I just being lazy?", "Mental Health"),
    ("Why do I get so irritable when I’m low, even if I catch it early?", "Mental Health"),
    ("How do I manage social anxiety when people constantly ask about my diabetes?", "Mental Health"),
    ("Does constantly tracking my glucose make me more anxious, or is it just necessary vigilance?", "Mental Health"),
    ("How do I handle the mental toll of needing to think about food all the time?", "Mental Health"),
    ("Is it normal to feel disconnected from my body when my blood sugar is really high?", "Mental Health"),
   
    ("How can I cope with diabetes burnout when I'm tired of constant blood sugar monitoring?", "Mental Health"),
    ("What strategies help with the anxiety I feel when my blood sugar drops unexpectedly?", "Mental Health"),
    ("How do I deal with feelings of guilt after episodes of high blood sugar?", "Mental Health"),
    ("What can I do about depression symptoms that seem worse when my blood sugars are fluctuating?", "Mental Health"),
    ("How can I manage the constant mental load of carb counting and insulin calculations?", "Mental Health"),
    ("What are healthy ways to respond to unsolicited diabetes advice that makes me feel judged?", "Mental Health"),
    ("How can I explain diabetes distress to my friends and family who don't understand?", "Mental Health"),
    ("What techniques help with the fear of hypoglycemia that keeps me from sleeping well?", "Mental Health"),
    ("How can I build confidence in managing my diabetes in social situations without feeling self-conscious?", "Mental Health"),
    ("What are ways to cope with grief about diabetes-related complications I'm experiencing?", "Mental Health"),
    ("How can I manage the anxiety I feel before doctor appointments when I'm worried about my A1C results?", "Mental Health"),
    ("What mindfulness techniques might help me stay present rather than worrying about future complications?", "Mental Health"),
    ("How can I maintain a positive body image when dealing with insulin pump and CGM devices?", "Mental Health"),
    ("What strategies help with the emotional impact of diabetes technology alarms disrupting my day?", "Mental Health"),
    ("How can I address feelings of being different or isolated because of my diabetes?", "Mental Health"),
    ("What can I do when diabetes management feels overwhelming and I'm experiencing panic attacks?", "Mental Health"),
    ("How might I recognize and address depression symptoms that could be affecting my diabetes management?", "Mental Health"),
    ("What are healthy ways to talk to my children about my diabetes without causing them anxiety?", "Mental Health"),
    ("How can I build resilience to handle the unpredictability of Type 1 diabetes day after day?", "Mental Health"),
    ("What strategies help with the frustration of unexplained blood sugar fluctuations despite doing everything 'right'?", "Mental Health"),
    ("I feel so lonely living with diabetes and feel like nobody understands me", "Mental Health")

]

# Save to CSV file
csv_filename = "diabetes_queries.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Query", "Category"])  # Write header
    writer.writerows(queries)  # Write data

print(f"CSV file '{csv_filename}' saved successfully!")
