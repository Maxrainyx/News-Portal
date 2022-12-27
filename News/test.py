""" def post(self, request, *args, **kwargs):
        categories = request.POST['category']
        users = Category.subscribers
        user_list = []
        for user in users:
            user_list.append(user)
        text = request.POST['text']

        if user_list:
            send_mail(
                subject=f'Новая запись в категориях: {categories}!',
                # имя клиента и дата записи будут в теме для удобства
                message=text,  # сообщение с кратким описанием проблемы
                from_email='maxrainyx@yandex.ru',
                # здесь указываете почту, с которой будете отправлять (об этом попозже)
                recipient_list=user_list  # здесь список получателей. Например, секретарь, сам врач и т. д.
            )
            # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же."""