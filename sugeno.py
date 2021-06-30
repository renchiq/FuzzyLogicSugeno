import random

from matplotlib import pyplot as plt


def membership_function(x, y):
    attendance_dict = {elem: 0 for elem in attendance}
    lecture_notes_dict = {elem: 0 for elem in lecture_notes}

    if x <= 25:
        attendance_dict['Rare'] = 1
    elif x >= 75:
        attendance_dict['Frequent'] = 1
    elif 25 < x <= 50:
        attendance_dict['Rare'] = (50 - x) / 25
        attendance_dict['Moderate'] = (x - 25) / 25
    elif 50 < x < 75:
        attendance_dict['Frequent'] = (x - 50) / 25
        attendance_dict['Moderate'] = (75 - x) / 25

    if y <= 50:
        if y >= 25:
            lecture_notes_dict['Low'] = (50 - y) / 50
            lecture_notes_dict['Medium'] = (y - 25) / 25
        elif y < 25:
            lecture_notes_dict['Low'] = (50 - y) / 50
    elif y > 50:
        if y <= 75:
            lecture_notes_dict['High'] = (y - 50) / 50
            lecture_notes_dict['Medium'] = (75 - y) / 25
        elif y > 75:
            lecture_notes_dict['High'] = (y - 50) / 50
    return attendance_dict, lecture_notes_dict


def aggregation(x, y):
    att_affiliations, lec_not_affiliations = membership_function(x, y)
    result = []
    for key_a, value_a in att_affiliations.items():
        for key_l, value_l in lec_not_affiliations.items():
            result.append([key_a, key_l, min(value_l, value_a)])
    # print("Результат этапа агрегирования: ", *result, sep='\n')
    return result


def activation(x, y):
    result = {
        'Rare': {
            'Low': "0.15 * u_X + 0.1 * u_Y",
            'Medium': "0.3 * u_X + 0.2 * u_Y",
            'High': "0.3 * u_X + 0.2 * u_Y"
        },
        'Moderate': {
            'Low': "0.3 * u_X + 0.3 * u_Y",
            'Medium': "0.35 * u_X + 0.4 * u_Y",
            'High': "0.55 * u_X + 0.3 * u_Y"
        },
        'Frequent': {
            'Low': "0.4 * u_X + 0.45 * u_Y",
            'Medium': "0.5 * u_X + 0.33 * u_Y",
            'High': "0.5 * u_X + 0.5 * u_Y"
        }
    }
    for key_x, value_y_function in result.items():
        for key_y, value_function in value_y_function.items():
            result[key_x][key_y] = eval(value_function,
                                        {'u_X': membership_function(x, y)[0][key_x],
                                         'u_Y': membership_function(x, y)[1][key_y]})
    # print("Результат этапа активации: ", result, sep='\n')
    return result


def defuzzification(x, y):
    acti = activation(x, y)
    aggr = aggregation(x, y)
    numerator = 0
    denominator = 0
    for aggregated_rule in aggr:
        numerator += aggregated_rule[2] * acti[aggregated_rule[0]][aggregated_rule[1]]
        denominator += aggregated_rule[2]
    return numerator / denominator


def build_membership_plots():
    attendance_plot_points = {
        'Rare': {
            'X': [],
            'Y': []
        },
        'Moderate': {
            'X': [],
            'Y': []
        },
        'Frequent': {
            'X': [],
            'Y': []
        }
    }

    for x in range(0, 101):
        if x <= 25:
            attendance_plot_points['Rare']['X'].append(x)
            attendance_plot_points['Rare']['Y'].append(1)
        elif x >= 75:
            attendance_plot_points['Frequent']['X'].append(x)
            attendance_plot_points['Frequent']['Y'].append(1)
        elif 25 < x <= 50:
            attendance_plot_points['Rare']['X'].append(x)
            attendance_plot_points['Moderate']['X'].append(x)
            attendance_plot_points['Rare']['Y'].append((50 - x) / 25)
            attendance_plot_points['Moderate']['Y'].append((x - 25) / 25)
        elif 50 < x < 75:
            attendance_plot_points['Frequent']['X'].append(x)
            attendance_plot_points['Moderate']['X'].append(x)
            attendance_plot_points['Frequent']['Y'].append((x - 50) / 25)
            attendance_plot_points['Moderate']['Y'].append((75 - x) / 25)

    note_taking_plot_points = {
        'Low': {
            'X': [],
            'Y': []
        },
        'Medium': {
            'X': [],
            'Y': []
        },
        'High': {
            'X': [],
            'Y': []
        }
    }

    for x in range(0, 101):
        if x <= 50:
            if x >= 25:
                note_taking_plot_points['Low']['X'].append(x)
                note_taking_plot_points['Medium']['X'].append(x)
                note_taking_plot_points['Low']['Y'].append((50 - x) / 50)
                note_taking_plot_points['Medium']['Y'].append((x - 25) / 25)
            elif x < 25:
                note_taking_plot_points['Low']['X'].append(x)
                note_taking_plot_points['Low']['Y'].append((50 - x) / 50)
        elif x > 50:
            if x <= 75:
                note_taking_plot_points['High']['X'].append(x)
                note_taking_plot_points['Medium']['X'].append(x)
                note_taking_plot_points['High']['Y'].append((x - 50) / 50)
                note_taking_plot_points['Medium']['Y'].append((75 - x) / 25)
            elif x > 75:
                note_taking_plot_points['High']['X'].append(x)
                note_taking_plot_points['High']['Y'].append((x - 50) / 50)

    fig = plt.figure()

    ax_1 = fig.add_subplot(1, 2, 1)
    ax_2 = fig.add_subplot(1, 2, 2)

    ax_1.set(xlabel='Уровень посещаемости',
             ylabel='Функция принадлежности')
    ax_2.set(xlabel='Уровень конспектирования',
             ylabel='Функция принадлежности')

    ax_1.set(title='Посещаемость лекций')
    ax_2.set(title='Конспектирование лекций')

    ax_1.plot(attendance_plot_points['Rare']['X'],
              attendance_plot_points['Rare']['Y'],
              label="Rare", lw=5, color='#A60000')
    ax_1.plot(attendance_plot_points['Moderate']['X'],
              attendance_plot_points['Moderate']['Y'],
              label="Moderate", lw=5, color='#06266F')
    ax_1.plot(attendance_plot_points['Frequent']['X'],
              attendance_plot_points['Frequent']['Y'],
              label="Frequent", lw=5, color='#A6A600')

    ax_2.plot(note_taking_plot_points['Low']['X'],
              note_taking_plot_points['Low']['Y'],
              label="Rare", lw=5, color='#FFAA00')
    ax_2.plot(note_taking_plot_points['Medium']['X'],
              note_taking_plot_points['Medium']['Y'],
              label="Moderate", lw=5, color='#7109AA')
    ax_2.plot(note_taking_plot_points['High']['X'],
              note_taking_plot_points['High']['Y'],
              label="Frequent", lw=5, color='#00CC00')

    plt.show()


def build_3d_plot():
    plt.clf()

    ax = plt.axes(projection="3d")

    x_points = []
    y_points = []
    z_points = []

    for x in range(0, 101):
        for y in range(0, 101):
            # if x not in y_points and y not in x_points:
            x_points.append(x)
            y_points.append(y)
            z_points.append(defuzzification(x, y))

    ax.set_title("Fuzzy Interference Graph Sugeno")
    ax.set_xlabel('Attendance')
    ax.set_ylabel('Lecture_noting')
    ax.set_zlabel('Lecture_quality')

    ax.plot_trisurf(x_points, y_points, z_points, cmap='winter', linewidth=0.5)

    plt.show()


def build_2d_plots():
    # note-taking is random-fixed
    # attendance is in range [0, 100]
    note_taking_value = random.randrange(1, 101)
    attendance_value = []
    defuzz_value = []
    for i in range(0, 101):
        attendance_value.append(i)
        defuzz_value.append(defuzzification(i, note_taking_value))
    fig = plt.figure()
    ax_1 = fig.add_subplot(1, 2, 1)
    ax_1.set(title="Note-taking = {0}".format(note_taking_value),
             xlabel="Attendance",
             ylabel="Membership")
    ax_1.plot(attendance_value,
              defuzz_value,
              lw=5, color='#000000')
    # note-taking is in range [0, 100]
    # attendance is random-fixed
    attendance_value = random.randrange(1, 101)
    note_taking_value = []
    defuzz_value = []
    for i in range(0, 101):
        note_taking_value.append(i)
        defuzz_value.append(defuzzification(i, attendance_value))
    ax_2 = fig.add_subplot(1, 2, 2)
    ax_2.set(title="Attendance = {0}".format(attendance_value),
             xlabel="Note-taking",
             ylabel="Membership")
    ax_2.plot(note_taking_value,
              defuzz_value,
              lw=5, color='#000000')
    plt.show()


if __name__ == "__main__":
    attendance = ['Rare', 'Moderate', 'Frequent']
    lecture_notes = ['Low', 'Medium', 'High']

    """
    Rule1:
        If X(Attendance) is Rare and Y(Lecture_notes) is Low then Z = 0.15 * u(X) + 0.1 * u(Y)
    Rule2:
        If X(Attendance) is Rare and Y(Lecture_notes) is Medium then Z = 0.3 * u(X) + 0.2 * u(Y)
    Rule3:
        If X(Attendance) is Rare and Y(Lecture_notes) is High then Z = 0.3 * u(X) + 0.2 * u(Y)
    Rule4:
        If X(Attendance) is Moderate and Y(Lecture_notes) is Low then Z = 0.3 * u(X) + 0.35 * u(Y)
    Rule5:
        If X(Attendance) is Moderate and Y(Lecture_notes) is Medium then Z = 0.35 * u(X) + 0.4 * u(Y)
    Rule6:
        If X(Attendance) is Moderate and Y(Lecture_notes) is High then Z = 0.55 * u(X) + 0.3 * u(Y)
    Rule7:
        If X(Attendance) is Frequent and Y(Lecture_notes) is Low then Z = 0.4 * u(X) + 0.45 * u(Y)
    Rule8:
        If X(Attendance) is Frequent and Y(Lecture_notes) is Medium then Z = 0.5 * u(X) + 0.33 * u(Y)
    Rule9:
        If X(Attendance) is Frequent and Y(Lecture_notes) is High then Z = 0.5 * u(X) + 0.5 * u(Y)
    """

    print('Отображение графиков функций принадлежности...')
    build_membership_plots()
    print('Построение 3D графика зависимости выходной лингвистической переменной...')
    build_3d_plot()
    print('Построение 2D графиков...')
    build_2d_plots()
    X = int(input('Введите значение первой входной лингвистической переменной(Х): '))
    Y = int(input('Введите значение второй входной лингвистической переменной(Y): '))
    print("Значения функций принадлежности для ЛП \"Посещаемость лекций\": {0}\n"
          "Значения функций принадлежности для ЛП \"Конспектирование лекций\": {1}".format(membership_function(X, Y)[0],
                                                                                           membership_function(X, Y)[1]))
    print('Значение выходной логистической переменной равно: ', defuzzification(X, Y) * 100)
