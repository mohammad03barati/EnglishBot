import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Content dictionary (unchanged from previous response)
CONTENT = {
    "A1": {
        "grammar": {
            "1": "A1 Grammar Lesson 1: Present Simple\n\n- Use for habits and facts.\n- Add s with he, she, it.\nExamples:\n1. I play every day.\n2. She reads books.",
            "2": "A1 Grammar Lesson 2: Present Continuous\n\n- Use for actions happening now.\n- Form: am/is/are + verb + ing.\nExamples:\n1. I am writing a message.\n2. He is watching TV.",
            "3": "A1 Grammar Lesson 3: Past Simple\n\n- Use for finished actions.\n- Add ed to regular verbs.\nExamples:\n1. I walked to school yesterday.\n2. She talked to her friend.",
            "4": "A1 Grammar Lesson 4: Simple Questions\n\n- Use do/does for present, did for past.\nExamples:\n1. Do you like coffee?\n2. Did she go home?",
            "5": "A1 Grammar Lesson 5: Prepositions of Place\n\n- Use to show where things are.\nExamples:\n1. The cat is on the table.\n2. My book is in the bag.",
            "6": "A1 Grammar Lesson 6: Basic Sentence Structures\n\n- Subject + Verb (+ Object).\nExamples:\n1. I eat apples.\n2. She likes music.",
            "7": "A1 Grammar Lesson 7: Possessive Forms\n\n- Use ’s or possessive adjectives (my, your).\nExamples:\n1. This is John’s book.\n2. It’s my house.",
            "8": "A1 Grammar Lesson 8: Countable and Uncountable\n\n- Countable: can count (e.g., apples).\n- Uncountable: cannot count (e.g., water).\nExamples:\n1. I have three apples (countable).\n2. I need some water (uncountable)."
        },
        "vocab": {
            "1": "A1 Vocab Lesson 1: Words 1-50\n\n1. I - من\n2. you - تو\n3. he - او (مرد)\n4. she - او (زن)\n5. it - آن\n6. we - ما\n7. they - آنها\n8. am - هستم\n9. is - است\n10. are - هستند\n11. have - دارم\n12. has - دارد\n13. do - انجام می‌دهم\n14. does - انجام می‌دهد\n15. go - می‌روم\n16. goes - می‌رود\n17. see - می‌بینم\n18. saw - دیدم\n19. eat - می‌خورم\n20. ate - خوردم\n21. drink - می‌نوشم\n22. drank - نوشیدم\n23. sleep - می‌خوابم\n24. slept - خوابیدم\n25. walk - راه می‌روم\n26. walked - راه رفتم\n27. run - می‌دوم\n28. ran - دویدم\n29. say - می‌گویم\n30. said - گفتم\n31. want - می‌خواهم\n32. wanted - خواستم\n33. like - دوست دارم\n34. liked - دوست داشتم\n35. love - عاشقم\n36. loved - عاشق بودم\n37. know - می‌دانم\n38. knew - می‌دانستم\n39. think - فکر می‌کنم\n40. thought - فکر کردم\n41. come - می‌آیم\n42. came - آمدم\n43. get - می‌گیرم\n44. got - گرفتم\n45. give - می‌دهم\n46. gave - دادم\n47. take - می‌برم\n48. took - بردم\n49. make - می‌سازم\n50. made - ساختم",
            "2": "A1 Vocab Lesson 2: Words 51-100\n\n51. time - زمان\n52. day - روز\n53. night - شب\n54. morning - صبح\n55. evening - عصر\n56. now - حالا\n57. today - امروز\n58. tomorrow - فردا\n59. yesterday - دیروز\n60. week - هفته\n61. month - ماه\n62. year - سال\n63. house - خانه\n64. room - اتاق\n65. door - در\n66. window - پنجره\n67. table - میز\n68. chair - صندلی\n69. bed - تخت\n70. car - ماشین\n71. book - کتاب\n72. pen - قلم\n73. paper - کاغذ\n74. school - مدرسه\n75. teacher - معلم\n76. student - دانش‌آموز\n77. friend - دوست\n78. family - خانواده\n79. mother - مادر\n80. father - پدر\n81. sister - خواهر\n82. brother - برادر\n83. child - کودک\n84. man - مرد\n85. woman - زن\n86. people - مردم\n87. name - نام\n88. good - خوب\n89. bad - بد\n90. big - بزرگ\n91. small - کوچک\n92. new - جدید\n93. old - قدیمی\n94. happy - خوشحال\n95. sad - غمگین\n96. yes - بله\n97. no - خیر\n98. here - اینجا\n99. there - آنجا\n100. where - کجا",
            "3": "A1 Vocab Lesson 3: Words 101-150\n\n101. what - چه\n102. who - کی\n103. when - کی\n104. why - چرا\n105. how - چگونه\n106. one - یک\n107. two - دو\n108. three - سه\n109. four - چهار\n110. five - پنج\n111. six - شش\n112. seven - هفت\n113. eight - هشت\n114. nine - نه\n115. ten - ده\n116. red - قرمز\n117. blue - آبی\n118. green - سبز\n119. yellow - زرد\n120. black - سیاه\n121. white - سفید\n122. food - غذا\n123. water - آب\n124. milk - شیر\n125. bread - نان\n126. apple - سیب\n127. orange - پرتقال\n128. eat - خوردن\n129. drink - نوشیدن\n130. cook - پختن\n131. hot - داغ\n132. cold - سرد\n133. in - در\n134. on - روی\n135. under - زیر\n136. next - کنار\n137. behind - پشت\n138. front - جلو\n139. up - بالا\n140. down - پایین\n141. left - چپ\n142. right - راست\n143. home - خانه\n144. work - کار\n145. play - بازی\n146. read - خواندن\n147. write - نوشتن\n148. listen - گوش دادن\n149. speak - صحبت کردن\n150. look - نگاه کردن",
            "4": "A1 Vocab Lesson 4: Words 151-200\n\n151. open - باز کردن\n152. close - بستن\n153. buy - خریدن\n154. sell - فروختن\n155. live - زندگی کردن\n156. need - نیاز داشتن\n157. use - استفاده کردن\n158. help - کمک کردن\n159. call - صدا کردن\n160. ask - پرسیدن\n161. answer - جواب دادن\n162. start - شروع کردن\n163. stop - متوقف کردن\n164. wait - منتظر ماندن\n165. find - پیدا کردن\n166. lose - گم کردن\n167. sit - نشستن\n168. stand - ایستادن\n169. drive - رانندگی کردن\n170. ride - سوار شدن\n171. fly - پرواز کردن\n172. swim - شنا کردن\n173. dance - رقصیدن\n174. sing - آواز خواندن\n175. laugh - خندیدن\n176. cry - گریه کردن\n177. fast - سریع\n178. slow - آهسته\n179. high - بلند\n180. low - کوتاه\n181. long - دراز\n182. short - کوتاه\n183. money - پول\n184. job - شغل\n185. city - شهر\n186. country - کشور\n187. street - خیابان\n188. park - پارک\n189. shop - مغازه\n190. market - بازار\n191. morning - صبح\n192. afternoon - بعدازظهر\n193. evening - عصر\n194. night - شب\n195. always - همیشه\n196. sometimes - گاهی\n197. never - هرگز\n198. again - دوباره\n199. please - لطفاً\n200. thank - تشکر"
        },
        "stories": {
            "1": "A1 Story 1: My Family\n\nMy family is big. I have a mother, a father, a sister, and a brother. We live in a house in the city. The house has three rooms. My room is small, but I like it. Every day, we eat bread and drink milk in the kitchen. Yesterday, my sister asked, “Do you want an apple?” I said, “Yes, please.” She gave me a red apple. My father works at a school—he is a teacher. My mother cooks food every day. Does she like it? Yes, she does. We walk to the park behind our house sometimes. We sit on chairs and look at trees. I love my family.",
            "2": "A1 Story 2: The Cat on the Chair\n\nA cat is sitting on a chair in my house. It is small and black. I like it a lot. Yesterday, it slept under the table for a long time. Now, it is looking at me. Does it want food? I think so. I give it some milk in a glass. The cat drinks it fast. My brother asked, “Where is the cat?” I said, “It’s on the chair.” He walked to the room and saw it. The cat ran to the window and is next to the bed now. My mother has a book about cats—she read it yesterday. The cat is my friend.",
            "3": "A1 Story 3: A Good Day\n\nToday, I am walking to school. The sun is yellow and hot. I see my friend on the street—we talked yesterday about books. My bag is on my back—it’s my bag with two books and a pen. I like school. The teacher is a good woman and teaches us every day. Do you go to school? Yes, I do. Yesterday, I played in the park after school—I ran fast and sat under a tree. Now, I am writing in my book. The day is good. Tomorrow, I want to read more. My friend is happy too.",
            "4": "A1 Story 4: The Market\n\nI go to the market every week—it is in the city. I buy apples, bread, and some water. Yesterday, I lost my money behind the shop. Did I find it? Yes, I did! I looked under the table and saw it. The market has many people. A man sells oranges—I asked, “How many do you have?” He said, “Ten.” I took three oranges. My bag is big—I put the food in it. My sister likes apples and ate one yesterday. Now, I am walking home. The sun is up in the sky.",
            "5": "A1 Story 5: The Teacher’s Book\n\nThe teacher has a book on her table—she is reading it now. The book is big and green. I am sitting in the classroom. I asked, “Where is your pen?” She said, “It’s in my bag under the chair.” Yesterday, she gave us two books—I read one at home. Do I like it? Yes, I do. The teacher is a good woman and helps us every day. My friend is writing now—he has a pen and some paper. The classroom has five chairs and one table. I like school a lot.",
            "6": "A1 Story 6: Two Apples\n\nI have two apples—they are red and small. I eat one now. Some milk is in a glass on the table. Yesterday, I drank milk and ate bread. Do I like apples? Yes, I do. My brother is in the kitchen—he is cooking food and has three oranges. I asked, “Where is your apple?” He said, “It’s behind the chair.” I looked and saw a yellow apple. We sit in the kitchen every day. My mother makes good food. I love milk and apples so much.",
            "7": "A1 Story 7: My Room\n\nMy room is small—the bed is next to the window. I am sleeping now because it is night. Yesterday, I walked in the park behind my house. This is my room—it has a chair and a table. Does it have a book? Yes, it does—the book is on the table. I read it every day. My sister is in her room—she is writing a letter. My father asked, “Where is your pen?” I said, “It’s in my bag under the bed.” I like my room—it’s quiet and nice.",
            "8": "A1 Story 8: The Dog under the Tree\n\nA dog is under a tree in the park—it runs fast every day. I saw it yesterday—did it play? Yes, it played in the grass. I give it some water in a bowl. It’s John’s dog and it is brown. My friend is walking with me now—we see the dog. He asked, “Where is the dog?” I said, “It’s under the tree.” The dog is sitting now—it has a ball next to it. Yesterday, I took the ball and gave it to the dog. We like dogs a lot.",
            "9": "A1 Story 9: A Happy Child\n\nA child is happy today—he is playing in the park in the morning. He has three books and two pens. Yesterday, he read one book on a chair. Where is his mother? She is on the chair next to him—she is reading too. I asked, “Do you like the park?” He said, “Yes, I do.” The park is big with many trees and some water. The child runs to the water—he drank some yesterday. Now, he is sitting under a tree. I like happy children.",
            "10": "A1 Story 10: The Car\n\nI want a car—it is big and blue. My father drives it every day. We went to the city yesterday—the car is in front of the house now. Do you like cars? I do. My brother is in the car—he is looking at a book. My mother asked, “Where is your bag?” I said, “It’s in the car.” The bag has two apples and some water. Yesterday, I walked to the shop and bought bread. Today, we eat in the car—it’s my father’s car. I love it."
        }
    },
    "A2": {
        "grammar": {
            "1": "A2 Grammar Lesson 1: Simple Past\n\n- Use for finished actions.\n- Add ed or use irregular forms.\nExamples:\n1. I visited my friend.\n2. She bought a bag.",
            "2": "A2 Grammar Lesson 2: Present Perfect\n\n- Use for past experiences.\n- Form: have/has + past participle.\nExamples:\n1. I have seen that movie.\n2. He has finished work.",
            "3": "A2 Grammar Lesson 3: Future Simple\n\n- Use will for plans.\nExamples:\n1. I will call you.\n2. She will go out.",
            "4": "A2 Grammar Lesson 4: Comparatives and Superlatives\n\n- Comparatives: er or more.\n- Superlatives: est or most.\nExamples:\n1. This is bigger than that.\n2. She’s the tallest.",
            "5": "A2 Grammar Lesson 5: Modals (can, should, must)\n\n- Can: ability.\n- Should: advice.\n- Must: need.\nExamples:\n1. I can swim.\n2. You should study.",
            "6": "A2 Grammar Lesson 6: Quantifiers (some, any, a lot of)\n\n- Some: positive.\n- Any: negative/questions.\nExamples:\n1. I have some books.\n2. No any milk.",
            "7": "A2 Grammar Lesson 7: Prepositions of Time and Place\n\n- At, in, on.\nExamples:\n1. I wake at 7.\n2. She lives in a city."
        },
        "vocab": {
            "1": "A2 Vocab Lesson 1: Words 1-50\n\n1. after - بعد از\n2. before - قبل از\n3. because - زیرا\n4. but - اما\n5. or - یا\n6. then - سپس\n7. also - همچنین\n8. maybe - شاید\n9. often - اغلب\n10. usually - معمولاً\n11. early - زود\n12. late - دیر\n13. soon - به زودی\n14. already - قبلاً\n15. still - هنوز\n16. visit - بازدید کردن\n17. travel - سفر کردن\n18. stay - ماندن\n19. leave - ترک کردن\n20. arrive - رسیدن\n21. wait - صبر کردن\n22. finish - تمام کردن\n23. start - شروع کردن\n24. try - تلاش کردن\n25. learn - یاد گرفتن\n26. study - درس خواندن\n27. teach - یاد دادن\n28. meet - ملاقات کردن\n29. talk - صحبت کردن\n30. tell - گفتن\n31. ask - پرسیدن\n32. answer - جواب دادن\n33. call - زنگ زدن\n34. send - فرستادن\n35. receive - دریافت کردن\n36. write - نوشتن\n37. read - خواندن\n38. listen - گوش دادن\n39. watch - تماشا کردن\n40. enjoy - لذت بردن\n41. feel - احساس کردن\n42. hope - امیدوار بودن\n43. need - نیاز داشتن\n44. want - خواستن\n45. decide - تصمیم گرفتن\n46. plan - برنامه‌ریزی کردن\n47. forget - فراموش کردن\n48. remember - به یاد آوردن\n49. understand - فهمیدن\n50. explain - توضیح دادن",
            "2": "A2 Vocab Lesson 2: Words 51-100\n\n51. place - مکان\n52. way - راه\n53. road - جاده\n54. village - روستا\n55. town - شهر کوچک\n56. country - کشور\n57. world - جهان\n58. trip - سفر\n59. holiday - تعطیلات\n60. weekend - آخر هفته\n61. party - مهمانی\n62. meeting - جلسه\n63. class - کلاس\n64. lesson - درس\n65. exam - امتحان\n66. job - شغل\n67. office - دفتر\n68. shop - مغازه\n69. restaurant - رستوران\n70. hotel - هتل\n71. train - قطار\n72. bus - اتوبوس\n73. plane - هواپیما\n74. ticket - بلیط\n75. bag - کیف\n76. clothes - لباس\n77. shoes - کفش\n78. hat - کلاه\n79. glasses - عینک\n80. key - کلید\n81. phone - تلفن\n82. email - ایمیل\n83. letter - نامه\n84. photo - عکس\n85. picture - تصویر\n86. music - موسیقی\n87. movie - فیلم\n88. game - بازی\n89. sport - ورزش\n90. team - تیم\n91. player - بازیکن\n92. ball - توپ\n93. food - غذا\n94. drink - نوشیدنی\n95. breakfast - صبحانه\n96. lunch - ناهار\n97. dinner - شام\n98. fruit - میوه\n99. vegetable - سبزی\n100. meat - گوشت",
            "3": "A2 Vocab Lesson 3: Words 101-150\n\n101. weather - هوا\n102. sun - خورشید\n103. rain - باران\n104. snow - برف\n105. wind - باد\n106. cloud - ابر\n107. hot - گرم\n108. cold - سرد\n109. warm - معتدل\n110. cool - خنک\n111. summer - تابستان\n112. winter - زمستان\n113. spring - بهار\n114. autumn - پاییز\n115. month - ماه\n116. week - هفته\n117. day - روز\n118. hour - ساعت\n119. minute - دقیقه\n120. second - ثانیه\n121. morning - صبح\n122. afternoon - بعدازظهر\n123. evening - عصر\n124. night - شب\n125. yesterday - دیروز\n126. today - امروز\n127. tomorrow - فردا\n128. always - همیشه\n129. sometimes - گاهی\n130. never - هرگز\n131. often - اغلب\n132. usually - معمولاً\n133. near - نزدیک\n134. far - دور\n135. left - چپ\n136. right - راست\n137. front - جلو\n138. back - پشت\n139. inside - داخل\n140. outside - بیرون\n141. above - بالای\n142. below - زیر\n143. between - بین\n144. next - کنار\n145. around - اطراف\n146. together - با هم\n147. alone - تنها\n148. different - متفاوت\n149. same - یکسان\n150. easy - آسان",
            "4": "A2 Vocab Lesson 4: Words 151-200\n\n151. difficult - دشوار\n152. beautiful - زیبا\n153. ugly - زشت\n154. clean - تمیز\n155. dirty - کثیف\n156. quiet - آرام\n157. noisy - پر سر و صدا\n158. safe - امن\n159. dangerous - خطرناک\n160. cheap - ارزان\n161. expensive - گران\n162. full - پر\n163. empty - خالی\n164. heavy - سنگین\n165. light - سبک\n166. tall - بلند\n167. short - کوتاه\n168. long - دراز\n169. young - جوان\n170. old - پیر\n171. fast - سریع\n172. slow - آهسته\n173. busy - مشغول\n174. free - آزاد\n175. tired - خسته\n176. hungry - گرسنه\n177. thirsty - تشنه\n178. sick - بیمار\n179. well - خوب\n180. happy - خوشحال\n181. sad - غمگین\n182. angry - عصبانی\n183. surprised - متعجب\n184. worried - نگران\n185. afraid - ترسیده\n186. excited - هیجان‌زده\n187. bored - خسته‌شده\n188. interested - علاقه‌مند\n189. famous - معروف\n190. important - مهم\n191. possible - ممکن\n192. impossible - غیرممکن\n193. true - درست\n194. false - نادرست\n195. right - صحیح\n196. wrong - اشتباه\n197. problem - مشکل\n198. idea - ایده\n199. question - سؤال\n200. answer - جواب"
        },
        "stories": {
            "1": "A2 Story 1: The Trip to the Sea\n\nLast summer, I visited my aunt in a village near the sea. I have been to the sea before, but this trip was better than the last one. The village is smaller than my town, but it’s the most beautiful place I know. I traveled by bus on a sunny day—it left at 9 in the morning. My aunt said, “You should swim in the sea.” I can swim well, so I went to the beach and swam for an hour. There were some people, but not a lot of them. Tomorrow, I will go again because I enjoyed it so much. My aunt cooked fish for dinner—it was the tastiest I have eaten. We watched a movie in her house at night. I stayed for three days. I must visit her again soon—it was fun!",
            "2": "A2 Story 2: My New Job\n\nI started a new job in an office last month. I have worked in a shop before, but this is busier than that. It’s the most important job I have had. I can use a computer, but I should learn more skills. My boss said, “You must arrive at 8 every day.” Yesterday, I finished early and went home at 4. There are a lot of papers on my desk, but no any free time. Tomorrow, I will meet my new team—they’re the friendliest people here, my boss says. I have seen the office kitchen—it’s cleaner than my house! I asked, “Can I bring food?” He said, “Yes.” I hope to stay for a long time.",
            "3": "A2 Story 3: The Rainy Day\n\nYesterday, it rained all day in my city. I have never seen so much rain—it was the worst weather this year! I stayed inside because I can’t go out in the rain. My sister said, “We should watch a movie.” We watched a funny one at home at 2 in the afternoon. Tomorrow, the sun will shine—it will be warmer than today. I have finished my homework, so I can play outside. There isn’t any snow, but a lot of water is on the road. I walked to the shop yesterday and bought some bread—my shoes got wetter than my coat! I must get an umbrella for rainy days. I hope it’s dry soon.",
            "4": "A2 Story 4: The Party\n\nLast weekend, I went to a party at my friend’s house. I have been to parties before, but this was the biggest one. The house is larger than mine, and the music was the loudest I have heard. I can dance, so I danced with some friends for hours. My friend said, “You should try the cake.” There was a lot of food, but no any juice—I drank water. Tomorrow, I will call her to say thank you. I have taken photos at the party—it started at 7 in the evening. We talked and laughed until midnight. I must sleep now—I’m tired. It was better than a usual night!",
            "5": "A2 Story 5: The Train Ride\n\nLast month, I took a train to a town for a holiday. I have traveled by bus before, but the train is faster than that. The town is prettier than my city—it’s the most beautiful place I have seen. I can read on the train, so I read a book. The ticket seller said, “You should sit near the window.” There were some people on the train, but not a lot of noise. Tomorrow, I will visit a museum there—I arrived at 3 in the afternoon. I have stayed in hotels before, but this one is cheaper. I must take photos for my family. I walked to the hotel—it was fun!",
            "6": "A2 Story 6: The Cooking Lesson\n\nYesterday, I had a cooking lesson at school. I have learned to cook rice before, but this was harder than that. The teacher said, “You should use some vegetables—they’re healthier than meat.” I can cook well, but I must be careful with the knife. We made a big meal in the kitchen at noon. There wasn’t any milk, but we had a lot of fruit. Tomorrow, I will try cooking at home. I have eaten our food—it was the tastiest! My friend helped me in the class—we finished at 2. The kitchen was cleaner after we worked. I love cooking now!",
            "7": "A2 Story 7: The Lost Bag\n\nLast week, I lost my bag in the park. I have never lost anything so important—it was the worst day! The bag is smaller than my school bag, but it has my phone and keys. I can look for it, so I went back at 5 in the evening. My brother said, “You should ask some people.” There wasn’t any help at first, but a man found it near a tree. Tomorrow, I will buy a new, bigger bag. I have thanked the man—he gave it to me. I must be more careful in the future. My phone was safer than I thought!",
            "8": "A2 Story 8: The Football Game\n\nLast Saturday, I played football in a park. I have played football before, but this game was the most exciting. Our team is better than the other team—we’re the strongest! I can run fast, but I should kick the ball more. The coach said, “You must practice at 4 every day.” There were a lot of players, but no any rain. Tomorrow, we will play again at the school. I scored a goal yesterday—my friends cheered for me, louder than usual. I have watched football on TV, but playing is more fun. I love sports!",
            "9": "A2 Story 9: The New Phone\n\nLast month, I bought a new phone at a shop. I have wanted one for a long time—it’s the best phone I have had. It’s smaller than my old phone, but more expensive. I can take photos with it—I should send some to my friends. The shop worker said, “You must charge it at night.” I have taken a lot of pictures already. Tomorrow, I will call my sister at 6 in the evening. I lost my old phone in the park once—it’s shinier now. I asked my father, “Can I buy a case?” He said, “Yes.” I love my phone!",
            "10": "A2 Story 10: The Holiday Plan\n\nLast year, I planned a holiday in a village. I have visited many places, but this village is the quietest. It’s smaller than my city, but more peaceful. I can stay for a week—I should take some books. My mother said, “You must leave at 8 in the morning.” I packed my bag yesterday—it has a lot of clothes, but no any shoes yet. Tomorrow, I will travel by train. I have never been on a train—it will be fun! I asked my friend, “Can you come?” He said, “No, I must work.” I hope to relax there!"
        }
    },
    "B1": {
        "grammar": {
            "1": "B1 Grammar Lesson 1: Past Perfect\n\n- Use for actions completed before another past action.\n- Form: had + past participle.\nExamples:\n1. I had finished my homework before dinner.\n2. She had left when he arrived.",
            "2": "B1 Grammar Lesson 2: First Conditional\n\n- Use for real future possibilities.\n- Form: If + present simple, will + base verb.\nExamples:\n1. If it rains, I will stay home.\n2. If you study, you will pass.",
            "3": "B1 Grammar Lesson 3: Second Conditional\n\n- Use for unreal or hypothetical situations.\n- Form: If + past simple, would + base verb.\nExamples:\n1. If I had money, I would travel.\n2. If she knew, she would tell us.",
            "4": "B1 Grammar Lesson 4: Relative Clauses\n\n- Use who, which, that to describe nouns.\nExamples:\n1. The man who lives next door is kind.\n2. The book which I read was great.",
            "5": "B1 Grammar Lesson 5: Reported Speech\n\n- Use to report what someone said.\n- Change tense and pronouns.\nExamples:\n1. She said that she was tired.\n2. He asked if I could help.",
            "6": "B1 Grammar Lesson 6: Modals of Possibility\n\n- Use might, could, may for possibility.\nExamples:\n1. It might rain later.\n2. She could be at home now."
        },
        "vocab": {
            "1": "B1 Vocab Lesson 1: Words 1-50\n\n1. achieve - دست یافتن\n2. advantage - مزیت\n3. argue - بحث کردن\n4. avoid - اجتناب کردن\n5. behavior - رفتار\n6. believe - باور کردن\n7. career - حرفه\n8. challenge - چالش\n9. choice - انتخاب\n10. compare - مقایسه کردن\n11. complain - شکایت کردن\n12. confident - مطمئن\n13. consider - در نظر گرفتن\n14. continue - ادامه دادن\n15. decision - تصمیم\n16. depend - بستگی داشتن\n17. describe - توصیف کردن\n18. develop - توسعه دادن\n19. discuss - بحث کردن\n20. effort - تلاش\n21. encourage - تشویق کردن\n22. expect - انتظار داشتن\n23. explain - توضیح دادن\n24. fail - شکست خوردن\n25. fear - ترس\n26. goal - هدف\n27. habit - عادت\n28. improve - بهبود دادن\n29. increase - افزایش دادن\n30. influence - تأثیر\n31. interest - علاقه\n32. involve - شامل شدن\n33. issue - مسئله\n34. join - پیوستن\n35. knowledge - دانش\n36. manage - مدیریت کردن\n37. mistake - اشتباه\n38. offer - پیشنهاد دادن\n39. opinion - نظر\n40. opportunity - فرصت\n41. plan - برنامه\n42. prepare - آماده کردن\n43. promise - قول دادن\n44. protect - محافظت کردن\n45. realize - متوجه شدن\n46. refuse - رد کردن\n47. regret - پشیمان شدن\n48. relationship - رابطه\n49. research - تحقیق\n50. respect - احترام",
            "2": "B1 Vocab Lesson 2: Words 51-100\n\n51. risk - ریسک\n52. satisfy - راضی کردن\n53. share - به اشتراک گذاشتن\n54. skill - مهارت\n55. solution - راه حل\n56. succeed - موفق شدن\n57. suggest - پیشنهاد کردن\n58. support - حمایت کردن\n59. surprise - تعجب\n60. trust - اعتماد\n61. understand - فهمیدن\n62. value - ارزش\n63. view - دیدگاه\n64. warn - هشدار دادن\n65. worry - نگران شدن\n66. advice - نصیحت\n67. agreement - توافق\n68. benefit - سود\n69. cause - علت\n70. chance - شانس\n71. condition - شرایط\n72. control - کنترل\n73. damage - آسیب\n74. danger - خطر\n75. deal - معامله\n76. difference - تفاوت\n77. difficulty - دشواری\n78. dream - رویا\n79. education - آموزش\n80. effect - اثر\n81. energy - انرژی\n82. environment - محیط زیست\n83. event - رویداد\n84. experience - تجربه\n85. fact - واقعیت\n86. feeling - احساس\n87. future - آینده\n88. health - سلامت\n89. history - تاریخ\n90. idea - ایده\n91. information - اطلاعات\n92. law - قانون\n93. level - سطح\n94. limit - محدودیت\n95. memory - حافظه\n96. nature - طبیعت\n97. need - نیاز\n98. news - خبر\n99. noise - سر و صدا\n100. peace - آرامش"
        },
        "stories": {
            "1": "B1 Story 1: The Job Interview\n\nSara had prepared for weeks before her job interview last month. She wanted a career in a company that offered good opportunities. If she got the job, she would move to the city. If she had stayed home, she wouldn’t have had this chance. The woman who interviewed her was kind but asked hard questions. Sara said that she had worked in a shop before and had learned many skills. The interviewer asked if Sara could start next week. Sara replied that she might need a few days to decide. After the interview, she felt confident—she could succeed in this role. Later, her friend told her, “I knew you’d do well!” Sara realized that all her effort had been worth it. She had never expected such a good result. Now, she’s waiting for their call and planning her future.",
            "2": "B1 Story 2: The Lost Phone\n\nAli had lost his phone before he went to the park yesterday. He thought he might have left it on the bus. If he found it, he would feel so relieved. If he had been more careful, this wouldn’t have happened. The man who drove the bus said, “Someone found a phone and gave it to me.” Ali described his phone—it was black with a blue case. The driver asked if Ali could come to the station later. Ali said that he had planned to meet a friend but would change his plans. There was a chance it could be his phone. When he got it back, he regretted not checking his bag earlier. His friend warned him to be more careful next time. Ali agreed and promised to improve his habits. He was happy to have his phone again.",
            "3": "B1 Story 3: The Surprise Party\n\nLila had organized a surprise party before her brother’s birthday last week. She hoped it might be the best party he’d ever had. If she planned it well, everyone would enjoy it. If she had told him, it wouldn’t have been a surprise. Her friend, who lived next door, helped with the food. Lila said that she had invited ten people and needed more chairs. Her friend asked if Lila could borrow some from her house. Lila replied that she might need to buy decorations too. The party was a success—her brother was shocked and happy. Later, he told her, “I didn’t expect this!” Lila felt proud because her effort had paid off. She decided to plan more events in the future. It was a night full of fun and laughter.",
            "4": "B1 Story 4: The Exam Day\n\nOmid had studied hard before his big exam yesterday. He knew that if he passed, he would get into university. If he had skipped his lessons, he wouldn’t have been ready. The teacher who wrote the exam was strict but fair. Omid said that he had reviewed all his notes the night before. His friend asked if he could finish on time. Omid answered that he might need every minute but felt prepared. During the test, he realized he could answer most questions. There was a chance he might even get a high score. After, his sister told him, “You’ve worked so hard!” Omid felt relieved when it was over. He had never been so nervous before. Now, he’s waiting for the results and hoping for good news.",
            "5": "B1 Story 5: The Holiday Plan\n\nMina had dreamed of a holiday before she started her new job last month. She thought she might go to the mountains—it could be relaxing. If she saved money, she would book a trip soon. If she had traveled earlier, she wouldn’t have had enough time off. The friend who went with her last year suggested a quiet village. Mina said that she had checked some hotels online already. Her friend asked if Mina could leave in two weeks. Mina replied that she might need to ask her boss first. There was a possibility it could work out perfectly. Later, her brother told her, “Take lots of photos!” Mina agreed and hoped to enjoy nature. She felt excited about the idea. It was time to turn her dream into reality."
        }
    },
    "B2": {
        "grammar": {
            "1": "B2 Grammar Lesson 1: Past Perfect Continuous\n\n- Use for ongoing actions before another past event.\n- Form: had been + verb + ing.\nExamples:\n1. I had been studying for hours before the exam.\n2. She had been working all day when he called.",
            "2": "B2 Grammar Lesson 2: Third Conditional\n\n- Use for unreal past situations and their results.\n- Form: If + had + past participle, would have + past participle.\nExamples:\n1. If I had known, I would have helped.\n2. If she had studied, she would have passed.",
            "3": "B2 Grammar Lesson 3: Passive Voice (All Tenses)\n\n- Use to focus on the action, not the doer.\nExamples:\n1. The room is cleaned daily (present).\n2. The project was completed on time (past).\n3. The report will be written tomorrow (future).",
            "4": "B2 Grammar Lesson 4: Mixed Conditionals\n\n- Combine past and present for hypothetical results.\nExamples:\n1. If I had studied, I would be more confident now.\n2. If she had saved money, she wouldn’t be broke today.",
            "5": "B2 Grammar Lesson 5: Inversion in Conditionals\n\n- Use for formal emphasis, omitting 'if'.\nExamples:\n1. Had I known, I would have acted differently.\n2. Were he here, we could discuss it.",
            "6": "B2 Grammar Lesson 6: Gerunds and Infinitives\n\n- Gerunds after some verbs, infinitives after others.\nExamples:\n1. I enjoy reading books (gerund).\n2. I decided to leave early (infinitive).",
            "7": "B2 Grammar Lesson 7: Reported Speech (All Tenses)\n\n- Report statements across all tenses.\nExamples:\n1. She said she had seen the movie.\n2. He asked what I was doing."
        },
        "vocab": {
            "1": "B2 Vocab Lesson 1: Words 1-50\n\n1. abolish - لغو کردن\n2. access - دسترسی\n3. adapt - سازگار شدن\n4. advocate - طرفداری کردن\n5. affect - تأثیر گذاشتن\n6. analysis - تحلیل\n7. assess - ارزیابی کردن\n8. authority - قدرت\n9. campaign - کمپین\n10. collapse - فروپاشی\n11. commit - متعهد شدن\n12. complex - پیچیده\n13. compromise - مصالحه\n14. conflict - تعارض\n15. consequence - نتیجه\n16. contribute - مشارکت کردن\n17. controversy - جنجال\n18. convince - متقاعد کردن\n19. debate - مناظره\n20. decline - کاهش یافتن\n21. demand - تقاضا\n22. deny - انکار کردن\n23. determine - تعیین کردن\n24. dilemma - دوراهی\n25. dominate - تسلط داشتن\n26. economy - اقتصاد\n27. emerge - ظهور کردن\n28. enforce - اجرا کردن\n29. estimate - تخمین زدن\n30. evidence - شواهد\n31. evolve - تکامل یافتن\n32. expand - گسترش دادن\n33. exploit - بهره‌برداری کردن\n34. factor - عامل\n35. fund - بودجه\n36. generate - تولید کردن\n37. guarantee - تضمین کردن\n38. implement - اجرا کردن\n39. imply - دلالت کردن\n40. impose - تحمیل کردن\n41. innovate - نوآوری کردن\n42. insight - بینش\n43. investigate - بررسی کردن\n44. justify - توجیه کردن\n45. legislation - قانون‌گذاری\n46. maintain - حفظ کردن\n47. negotiate - مذاکره کردن\n48. objective - هدف\n49. outcome - نتیجه\n50. participate - شرکت کردن",
            "2": "B2 Vocab Lesson 2: Words 51-100\n\n51. perspective - دیدگاه\n52. policy - سیاست\n53. principle - اصل\n54. promote - ترویج کردن\n55. propose - پیشنهاد کردن\n56. protest - اعتراض کردن\n57. pursue - دنبال کردن\n58. radical - افراطی\n59. reform - اصلاح\n60. regulate - تنظیم کردن\n61. reject - رد کردن\n62. rely - تکیه کردن\n63. resolve - حل کردن\n64. resource - منبع\n65. restrict - محدود کردن\n66. reveal - آشکار کردن\n67. revolution - انقلاب\n68. scope - محدوده\n69. sector - بخش\n70. significant - قابل توجه\n71. strategy - استراتژی\n72. submit - ارائه دادن\n73. sustain - پایدار کردن\n74. theory - تئوری\n75. transform - تغییر شکل دادن\n76. trend - روند\n77. undermine - تضعیف کردن\n78. unite - متحد کردن\n79. violate - نقض کردن\n80. welfare - رفاه\n81. break down - خراب شدن\n82. bring up - مطرح کردن\n83. carry out - انجام دادن\n84. cut off - قطع کردن\n85. figure out - فهمیدن\n86. give up - تسلیم شدن\n87. hold back - عقب نگه داشتن\n88. look into - بررسی کردن\n89. pick up - برداشتن\n90. run out - تمام شدن\n91. set up - راه‌اندازی کردن\n92. take over - تصاحب کردن\n93. turn down - رد کردن\n94. work out - حل کردن\n95. on the contrary - برعکس\n96. in the long run - در درازمدت\n97. by all means - به هر وسیله\n98. under pressure - تحت فشار\n99. out of the blue - ناگهانی\n100. piece of cake - کار آسان"
        },
        "stories": {
            "1": "B2 Story 1: The Failed Project\n\nBefore the deadline last month, the team had been working nonstop on a big project. Had they known about the budget cuts, they would have scaled it back. Instead, the project was abandoned after weeks of effort. If they had managed the funds better, they wouldn’t be in this mess now. I enjoy solving problems, but this time I decided to step back. My boss said that she had been planning to cancel it anyway due to a lack of resources. The report was being written when the news came—it was never finished. Looking into the issue, we found that costs had been underestimated. In the long run, this failure taught us to assess risks more carefully. A colleague proposed starting over, but it was turned down. The company is now negotiating a new strategy to avoid such collapses. I suggested carrying out a full review next time. It wasn’t a piece of cake, but we learned a lot.",
            "2": "B2 Story 2: The Political Debate\n\nLast year, I had been preparing for a debate on environmental policy when it was suddenly canceled. If I had participated, I would have advocated for stricter regulations. The event was being organized by a local group but was shut down due to protests. Had I spoken, I might have influenced the outcome—or so I like to think. I enjoy debating complex issues, but I decided to write an article instead. A friend said that she had been expecting a big turnout before the chaos started. If we had anticipated the opposition, we would be better prepared now. The policy is still being discussed in the media. Investigating the issue revealed deep divisions. I proposed setting up a new forum, but resources ran out. Under pressure, the group rejected my idea. In the end, I figured out that change takes time. It came out of the blue, but I’m not giving up.",
            "3": "B2 Story 3: The Business Decision\n\nBefore signing the contract last week, I had been researching the company for months. If I had known their reputation, I would have rejected the deal. The agreement was signed, and soon problems emerged. If I had acted differently, I wouldn’t be negotiating refunds now. I enjoy taking risks, but this time I decided to consult an expert. The expert said that he had been warning clients about this firm for years. The product was being tested when complaints poured in—it wasn’t ready. Looking into it, I found evidence of poor quality. Had we investigated more, we could have avoided losses. My partner suggested cutting off ties, and we did. The decision was justified by the outcome. We’re now working out a new plan to recover. It’s no piece of cake, but we’ll manage.",
            "4": "B2 Story 4: The Science Conference\n\nI had been preparing a presentation for a science conference before it was postponed last month. If I had delivered it, I would have shared new research on climate change. The event was being planned when funding was cut. Had I known earlier, I would have adapted my approach. I enjoy presenting complex theories, so I decided to submit it online instead. A colleague said that she had been expecting a big audience before the delay. If I had submitted earlier, I would be recognized now. The data is still being analyzed by peers. Investigating further, I found support for my ideas. I proposed holding a virtual session, and it was set up. Under pressure, I carried out last-minute edits. The feedback was significant—it’s pushing my work forward. On the contrary, the delay helped me refine it.",
            "5": "B2 Story 5: The Family Argument\n\nBefore the family meeting last weekend, we had been arguing about selling the house for weeks. If we had agreed earlier, we would have sold it by now. The decision was being debated when tempers flared. Had I stayed calm, I might have convinced them. I enjoy mediating, but this time I decided to listen instead. My sister said that she had been planning to move out anyway. If she had left sooner, we wouldn’t be so stressed now. Looking into the market, prices were dropping fast. I suggested compromising on a lower price, but it was turned down. We’re still figuring out what to do. Under pressure, I proposed renting it out instead. In the long run, that might work. It’s not easy, but we’ll resolve it somehow."
        }
    }
}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("A1 - Beginner", callback_data='level_A1')],
        [InlineKeyboardButton("A2 - Elementary", callback_data='level_A2')],
        [InlineKeyboardButton("B1 - Intermediate", callback_data='level_B1')],
        [InlineKeyboardButton("B2 - Upper Intermediate", callback_data='level_B2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose your level:", reply_markup=reply_markup)

# Handle button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('level_'):
        level = data.split('_')[1]
        keyboard = [
            [InlineKeyboardButton("Grammar", callback_data=f'{level}_grammar')],
            [InlineKeyboardButton("Vocabulary", callback_data=f'{level}_vocab')],
            [InlineKeyboardButton("Stories", callback_data=f'{level}_stories')],
            [InlineKeyboardButton("Back to Levels", callback_data='back_to_levels')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Level {level}: Choose an option:", reply_markup=reply_markup)

    elif data.endswith('_grammar'):
        level = data.split('_')[0]
        if level == 'A1':
            keyboard = [
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(1, 5)],
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(5, 9)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        elif level == 'A2':
            keyboard = [
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(1, 5)],
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(5, 8)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        elif level == 'B1':
            keyboard = [
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(1, 4)],
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(4, 7)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        elif level == 'B2':
            keyboard = [
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(1, 5)],
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_grammar_{i}') for i in range(5, 8)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"{level} Grammar Lessons:", reply_markup=reply_markup)

    elif data.endswith('_vocab'):
        level = data.split('_')[0]
        if level in ['A1', 'A2']:
            keyboard = [
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_vocab_{i}') for i in range(1, 5)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        elif level in ['B1', 'B2']:
            keyboard = [
                [InlineKeyboardButton(f"Lesson {i}", callback_data=f'{level}_vocab_{i}') for i in range(1, 3)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"{level} Vocabulary Lessons:", reply_markup=reply_markup)

    elif data.endswith('_stories'):
        level = data.split('_')[0]
        if level in ['A1', 'A2']:
            keyboard = [
                [InlineKeyboardButton(f"Story {i}", callback_data=f'{level}_story_{i}') for i in range(1, 6)],
                [InlineKeyboardButton(f"Story {i}", callback_data=f'{level}_story_{i}') for i in range(6, 11)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        elif level in ['B1', 'B2']:
            keyboard = [
                [InlineKeyboardButton(f"Story {i}", callback_data=f'{level}_story_{i}') for i in range(1, 6)],
                [InlineKeyboardButton("Back", callback_data=f'level_{level}')]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"{level} Stories:", reply_markup=reply_markup)

    elif data == 'back_to_levels':
        keyboard = [
            [InlineKeyboardButton("A1 - Beginner", callback_data='level_A1')],
            [InlineKeyboardButton("A2 - Elementary", callback_data='level_A2')],
            [InlineKeyboardButton("B1 - Intermediate", callback_data='level_B1')],
            [InlineKeyboardButton("B2 - Upper Intermediate", callback_data='level_B2')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Choose your level:", reply_markup=reply_markup)

    elif data.count('_') == 2:
        level, category, num = data.split('_')
        # Map 'story' to 'stories' for content lookup and back button
        content_category = 'stories' if category == 'story' else category
        content = CONTENT.get(level, {}).get(content_category, {}).get(num, "Content not found.")
        keyboard = [[InlineKeyboardButton(f"Back to {content_category.capitalize()}", callback_data=f'{level}_{content_category}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(content, reply_markup=reply_markup)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text("Oops! Something went wrong. Try /start again.")

# Main function
def main() -> None:
    token = "7589365578:AAErZ9vfkQcASAccPeDs0AX0NDwThJxD4oI"
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error)
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()