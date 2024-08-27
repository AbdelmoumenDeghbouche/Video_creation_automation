def calculate_subtitle_durations(audio_duration, all_script_words_list):
    """
    Calculate the durations of subtitles based on the audio duration and script words.

    Args:
        audio_duration (float): Duration of the audio in seconds.
        all_script_words_list (list): List of words in the script.

    Returns:
        list: Durations of each subtitle in seconds.
    """
    total_chars = sum(len(word) for word in all_script_words_list)
    durations = []

    for word in all_script_words_list:
        word_length = len(word)
        word_duration = (word_length / total_chars) * audio_duration
        durations.append(word_duration)
    print("durations of words : \n", durations)
    return durations


arabic_text = "محبي لعبة ببجي ، لماذا تضييع الوقت في اللعب من اجل الحصول على سكنات مملة مثل هذا السكن.... ، بدلا من ذلك حرب طريقة زوبا التي ستستغرق منك دقائق فقط و ستحصل على سكنات اسطورية مثل بذلة المعاقب الثلجي و بذلة الفرعون الاسطورية و حتى سكن الامفور الثلجي ، بمعنى آخر ، كل السكنات النادرة ستحصل عليها دون دفع اي قرش ، كل ما عليكم فعله هو نسخ الفيديو أولا ،و من ثم زيارة موقع Zoba dot games واختيارُ شعارِ بَابْجِي ثم إتِّبَاعُ الخطوات الموضحة في الموقع. لن تحتاجوا إلى توفير أي تكاليف ، فقط قوموا بإدخال مُعَرِّفِ اللاعب الID أو اسم المستخدم الخاص بكم في اللعبة. ومبروك عليكم. لا تقلقوا فهذا الموقع موثوق وآمن، فمن غير المنطقي أن يتم حَظْرُ حسابكم بسبب إدخال الID الخاص بكم فقط.و كالعادة لا تنسو زوبا الطيب من دعائكم الخير يا محبي"

calculate_subtitle_durations(57, arabic_text)
