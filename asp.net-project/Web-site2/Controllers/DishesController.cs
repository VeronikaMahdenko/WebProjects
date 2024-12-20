﻿using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Linq;
using Web_site2.Models;
using static System.Net.Mime.MediaTypeNames;

public class ServicesController : Controller
{
	private static List<Service> services = new List<Service>
	{
		new Service { Id = 1, Name = "Манікюр", Description = "Манікюр – це чудовий спосіб поєднати приємне з корисним. " +
			"Зберегти красу та свіжість рук у cучасних умовах дуже складно. Зараз це не примха, а щоденна необхідність. " +
			"Майстри салону допоможуть Вам у цьому. Вони підберуть гарну форму нігтів і колір покриття індивідуально під Ваш стиль, смаки або спосіб життя. " +
			"Манікюр складається із цілого комплексу різних приємних та корисних процедур, які гарантують відмінний результат." +
			" Разом із нами Ваші руки завжди будуть доглянуті та красиві.", ImageUrl = "Images\\nail.jpg" },
		new Service { Id = 2, Name = "Масаж", Description = "Всі ми знаємо, що профілактика хвороб ― це значно краще, ніж їх лікування." +
			" Під час професійного масажу стимулюється кровообіг і відтік лімфи з тканин, клітини організму насичуються киснем, а також підвищується рівень гістаміну та ендорфіну. " +
			"Не дарма ж масаж прописують при комплексній терапії проти багатьох хвороб. У світі існує безліч видів масажу, єдиної класифікації для цих оздоровчих процедур не придумали." +
			" Проте, який з масажів Ви б не обрали, слід пам'ятати головне правило: довіряйте лише спеціалістам. " +
			"Кваліфікований масажист у нашому салоні вміє правильно підібрати вид процедури, інтенсивність та тривалість. " +
			"Так, щоб по-справжньому принести Вам користь.", ImageUrl = "Images\\massage.jpg" },

		new Service { Id = 3, Name = "Брови та вії", Description = "На брови та вії завжди була певна мода. Форма брів завжди залежала від сучасних тенденцій та нових віянь. " +
			"І це цілком зрозуміло, тому що вони додають обличчю новий вираз, а також добре виглядають в тандемі з макіяжем. " +
			"Моделювання брів – це процедура, за допомогою якої можна змінити колір брів, їх форму, товщину і ширину. " +
			"Для цього потрібно враховувати форму обличчя, розріз очей, колір волосся, відтінок шкіри." +
			" Правильне моделювання форми брів додасть обличчю виразності і зробить брови акуратними і природними. " +
			"А визначити ідеальну для Вас форму допоможе наш майстер. А зробити ваш погляж більш виразним допоможе ламінування вій.", ImageUrl = "Images\\eyebrows.jpg" }
	};

	public IActionResult Index()
    {
        return View(services);
    }


}