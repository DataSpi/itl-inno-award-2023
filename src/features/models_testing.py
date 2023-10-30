from transformers import pipeline

task_list=['audio-classification', 'automatic-speech-recognition', 'conversational', 
      'depth-estimation', 'document-question-answering', 'feature-extraction', 
      'fill-mask', 'image-classification', 'image-segmentation', 'image-to-text', 
      'mask-generation', 'ner', 'object-detection', 'question-answering', 
      'sentiment-analysis', 'summarization', 'table-question-answering', 
      'text-classification', 'text-generation', 'text2text-generation', 
      'token-classification', 'translation', 'video-classification', 
      'visual-question-answering', 'vqa', 'zero-shot-audio-classification', 
      'zero-shot-classification', 'zero-shot-image-classification', 'zero-shot-object-detection', 
      'translation_XX_to_YY']

# -------------------------summarization-------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # I think this is a good summarizer
# pipe = pipeline("summarization", model="facebook/bart-large-cnn")#, tokenizer="t5-base"

ARTICLE = r""" New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
2010 marriage license application, according to court documents.
Prosecutors said the marriages were part of an immigration scam.
On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
"""
summary = summarizer(ARTICLE, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
print(summary)
# >>> [{'summary_text': 'Liana Barrientos, 39, is charged with two counts of "offering a false instrument for filing in the first degree" In total, she has been married 10 times, with nine of her marriages occurring between 1999 and 2002. She is believed to still be married to four men.'}]


# this is a paragraph from a Paul Graham's essay called "How to do great work"
paragraph =  """
The first step is to decide what to work on. The work you choose needs to have three qualities: it has to be something you have a natural aptitude for, that you have a deep interest in, and that offers scope to do great work.

In practice you don't have to worry much about the third criterion. Ambitious people are if anything already too conservative about it. So all you need to do is find something you have an aptitude for and great interest in. [1]

That sounds straightforward, but it's often quite difficult. When you're young you don't know what you're good at or what different kinds of work are like. Some kinds of work you end up doing may not even exist yet. So while some people know what they want to do at 14, most have to figure it out.

The way to figure out what to work on is by working. If you're not sure what to work on, guess. But pick something and get going. You'll probably guess wrong some of the time, but that's fine. It's good to know about multiple things; some of the biggest discoveries come from noticing connections between different fields.

Develop a habit of working on your own projects. Don't let "work" mean something other people tell you to do. If you do manage to do great work one day, it will probably be on a project of your own. It may be within some bigger project, but you'll be driving your part of it.

What should your projects be? Whatever seems to you excitingly ambitious. As you grow older and your taste in projects evolves, exciting and important will converge. At 7 it may seem excitingly ambitious to build huge things out of Lego, then at 14 to teach yourself calculus, till at 21 you're starting to explore unanswered questions in physics. But always preserve excitingness.

There's a kind of excited curiosity that's both the engine and the rudder of great work. It will not only drive you, but if you let it have its way, will also show you what to work on.
"""
# >>> [{'summary_text': "When you're young you don't know what you're good at or what different kinds of work are like. The way to figure out what to work on is by working. Whatever seems to you excitingly ambitious will converge."}]
summary = summarizer(paragraph, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
print(summary)

short_paragraph =  """
The first step is to decide what to work on. The work you choose needs to have three qualities: it has to be something you have a natural aptitude for, that you have a deep interest in, and that offers scope to do great work.

In practice you don't have to worry much about the third criterion. Ambitious people are if anything already too conservative about it. So all you need to do is find something you have an aptitude for and great interest in. [1]

That sounds straightforward, but it's often quite difficult. When you're young you don't know what you're good at or what different kinds of work are like. Some kinds of work you end up doing may not even exist yet. So while some people know what they want to do at 14, most have to figure it out.
"""
summary = pipe(short_paragraph, max_length=100, min_length=30, do_sample=False)
summary[0]['summary_text']

# -------------------------question-answering-------------------------
qa = pipeline(task='question-answering', model="deepset/roberta-base-squad2")
question = "tell me about earth"
context = """
The solar system is a vast collection of celestial bodies that are bound by gravity to the Sun. It consists of the Sun, eight planets, their moons, asteroids, comets, and other smaller objects.

Here's some information about each of the planets in the solar system:

Mercury: It is the closest planet to the Sun and the smallest planet in the solar system. It has a rocky surface and no atmosphere.

Venus: Venus is often called Earth's twin due to its similar size and composition. It has a thick atmosphere, which creates a runaway greenhouse effect and makes it the hottest planet in the solar system.

Earth: Our home planet, Earth, is the third planet from the Sun. It is the only planet known to support life. It has a diverse range of ecosystems and is characterized by its oceans, landmasses, and atmosphere.

Mars: Known as the "Red Planet," Mars is the fourth planet from the Sun. It has a thin atmosphere, polar ice caps, and surface features such as canyons, volcanoes, and the largest volcano in the solar system called Olympus Mons.

Jupiter: Jupiter is the largest planet in the solar system. It is a gas giant with a thick atmosphere and a prominent system of rings. It is known for its Great Red Spot, a persistent storm in its atmosphere.

Saturn: Saturn is another gas giant with a prominent ring system surrounding it. It is the second-largest planet in the solar system. Saturn is known for its beautiful and complex ring structure.

Uranus: Uranus is an ice giant, composed mostly of ices such as water, ammonia, and methane. It has a unique feature of rotating on its side, leading to extreme seasons.

Neptune: Neptune is the farthest planet from the Sun. It is also an ice giant and has a deep blue color due to the presence of methane in its atmosphere. It has strong winds and the fastest recorded wind speeds in the solar system.

These are the eight planets in the solar system, each with its own distinct characteristics and features.
"""
answer = qa({
    'question': question,
    'context': context
})

print(answer['answer'])


# -------------------------conversational-------------------------

conv = pipeline("conversational", model="llSourcell/medllama2_7b")
ques="what is HIV virus?"
# conv

# -------------------------text-generation-------------------------
texgen = pipeline("text-generation", model="TheBloke/Llama-2-7B-GPTQ")
generator = pipeline(task='text-generation', model="distilgpt2")
# generator = pipeline(task='text2text-generation', model="google/mt5-small")


text = """once upon a time, in the jungle, there is a boy"""
# generator(text)
print(generator(text)[0]['generated_text'])

# -------------------------vietnamese-------------------------
vnese = """
chúng ta đã có một khoảng thời gian bên nhau với nhiều loại cảm xúc. có lúc cao lúc thấp, 
tuy nhiên nhìn lại thì đó chắc chắn là một trải nghiệm đáng nhớ. 
anh có thể kết luận như vậy mà chẳng cần phải suy nghĩ. 
anh muốn mình sẽ nhớ nó, anh muốn mình sẽ nhớ em, nhiều nhất có thể. 
anh đoán là em cũng thế. 
vậy nên, có lẽ mình cần một cái gì đó để document lại khoảng thời gian mà mình đã dành cho nhau, 
hay ho một tý, đặc biệt một tý. và nó sẽ là cái này, 
nó sẽ là món quà sinh nhật tuổi 25 của em. 
anh cũng chưa biết cụ thể nó là cái gì đâu, nhưng anh cứ note ý tưởng này ở đây lại như vậy đã. 
"""
sample = """
The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, 
and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. 
During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, 
a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. 
It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial 
at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). 
Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in 
France after the Millau Viaduct.
"""

summary_text = summarizer(sample, max_length=70, min_length=30, do_sample=False)
print(summary_text[0]['summary_text'])



