# Import library Flet
import flet
from flet import *
import datetime
import mysql.connector

# Buat koneksi ke database SQL
koneksi_db = mysql.connector.connect(host="localhost", user="root", password="", database="fitness-calorie-center-bymth-db")
cursor = koneksi_db.cursor()

class FormUserFitness(UserControl):
    def build(user_fitness):
        # buat variabel inputan
        user_fitness.inputan_user_id = TextField(visible=False, expand=True)
        user_fitness.inputan_user_name = TextField(label="Username", hint_text="masukkan username ...", expand=True)
        user_fitness.inputan_user_age = TextField(label="Age", hint_text="masukkan age ...", expand=True)
        # Create a variable for the date input
        user_fitness.inputan_training_date = TextField(label="Training Date", read_only=True,expand=True)

        def ubah_tanggal(e):
            tgl_baru = user_fitness.opsi_tanggal.value
            user_fitness.inputan_training_date.value = str(tgl_baru)
            user_fitness.update()

        def opsi_tanggal_dismissed(e):
            user_fitness.update()

        # Create a date picker
        user_fitness.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal,
            on_dismiss=opsi_tanggal_dismissed,
            first_date=datetime.datetime(1945, 1, 1),
            last_date=datetime.date.today(),
        )

        # Create a button to open the date picker
        user_fitness.tgl_lahir_button = IconButton(
            icon=icons.DATE_RANGE_OUTLINED,
            icon_color=colors.GREEN,
            tooltip="Pilih Tanggal",
            on_click=lambda _: user_fitness.opsi_tanggal.pick_date(),
        )
        user_fitness.inputan_user_gender = Dropdown(
            label="Gender",
            options=[
                dropdown.Option("Male"),
                dropdown.Option("Female"),
            ],
            expand=True
        )
        user_fitness.inputan_user_weight = TextField(label="Weight", hint_text="masukkan weight ...", expand=True)
        user_fitness.inputan_user_height = TextField(label="Height", hint_text="masukkan height ...", expand=True)
        user_fitness.inputan_user_activity_level = Dropdown(
            label="Activity Level",
            options=[
            dropdown.Option("Low"),
            dropdown.Option("Moderate"),
            dropdown.Option("High"),
            ],
            expand=True
        )
        # Constants for BMR calculation
        # Constants for BMR calculation
        MALE_BMR_BASE = 88.362
        MALE_BMR_WEIGHT_FACTOR = 13.397
        MALE_BMR_HEIGHT_FACTOR = 4.799
        MALE_BMR_AGE_FACTOR = 5.677

        FEMALE_BMR_BASE = 447.593
        FEMALE_BMR_WEIGHT_FACTOR = 9.247
        FEMALE_BMR_HEIGHT_FACTOR = 3.098
        FEMALE_BMR_AGE_FACTOR = 4.330

        ACTIVITY_FACTORS = {
            "Low": 1.2,
            "Moderate": 1.55,
            "High": 1.725
        }

        # Fungsi untuk menghitung BMR menggunakan persamaan Mifflin-St Jeor
        def calculate_bmr(weight, height, age, gender):
            if gender == "Male":
                return (MALE_BMR_BASE + 
                        (MALE_BMR_WEIGHT_FACTOR * weight) + 
                        (MALE_BMR_HEIGHT_FACTOR * height) - 
                        (MALE_BMR_AGE_FACTOR * age))
            elif gender == "Female":
                return (FEMALE_BMR_BASE + 
                        (FEMALE_BMR_WEIGHT_FACTOR * weight) + 
                        (FEMALE_BMR_HEIGHT_FACTOR * height) - 
                        (FEMALE_BMR_AGE_FACTOR * age))

        # Fungsi untuk menghitung kebutuhan kalori berdasarkan BMR dan tingkat aktivitas
        def calculate_calories(bmr, activity_level):
            return bmr * ACTIVITY_FACTORS[activity_level]

        # Fungsi untuk mengupdate hasil perhitungan di UI
        def hitung_kalori(e):
            weight = float(user_fitness.inputan_user_weight.value)
            height = float(user_fitness.inputan_user_height.value)
            age = int(user_fitness.inputan_user_age.value)
            gender = user_fitness.inputan_user_gender.value
            activity_level = user_fitness.inputan_user_activity_level.value

            bmr = calculate_bmr(weight, height, age, gender)
            calories = calculate_calories(bmr, activity_level)
            
            user_fitness.hasil_hitungan_kalori.value = round(calories, 2)
            user_fitness.update()

        user_fitness.hasil_hitungan_kalori = TextField(
            on_change=hitung_kalori,
            label="Hasil Hitung Kalori",
            hint_text="Hasil Hitungan Kalori",
            read_only=True,
            suffix_text="kcal",  #Add the unit "kcal" to the text field
            expand=True
        )
        # Create a button to open the date picker
        user_fitness.hitung_kalori_button = IconButton(
            icon=icons.CALCULATE_SHARP,
            icon_color=colors.BLUE_200,
            tooltip="Hitung Kalori",
            on_click = hitung_kalori,
        )
               
        # Fungsi untuk menghitung Protein
        def calculate_protein(e):
            protein_goal = (float(user_fitness.hasil_hitungan_kalori.value) * 0.3) / 4  # 30% dari kalori untuk protein (1g protein = 4 kalori)
            user_fitness.hasil_hitungan_protein.value = round(protein_goal, 2)
            user_fitness.update()
            
                 
        user_fitness.hasil_hitungan_protein = TextField(
            on_change=calculate_protein,
            label="Hasil Hitung Protein",
            hint_text="Hasil Hitungan Protein",
            read_only=True,
            suffix_text="kcal",  #Add the unit "kcal" to the text field
            expand=True
        )
        # Create a button to open
        user_fitness.hitung_protein_button = IconButton(
            icon=icons.CALCULATE_SHARP,
            icon_color=colors.BLUE_200,
            tooltip="Hitung Protein",
            on_click = calculate_protein,
        )
        

        def calculate_carb(e):
            carb_goal = (float(user_fitness.hasil_hitungan_kalori.value) * 0.4) / 4  # 40% dari kalori untuk karbohidrat (1g karbohidrat = 4 kalori)
            user_fitness.hasil_hitungan_carb.value = round(carb_goal, 2)
            user_fitness.update()
        
        user_fitness.hasil_hitungan_carb = TextField(
            on_change=calculate_carb,
            label="Hasil Hitung Carbo",
            hint_text="Hasil Hitungan Carbo",
            read_only=True,
            suffix_text="kcal",  #Add the unit "kcal" to the text field
            expand=True
        )
        # Create a button to open
        user_fitness.hitung_carb_button = IconButton(
            icon=icons.CALCULATE_SHARP,
            icon_color=colors.BLUE_200,
            tooltip="Hitung Kalori",
            on_click = calculate_carb,
        )
        def calculate_fat(e):
            fat_goal = (float(user_fitness.hasil_hitungan_kalori.value) * 0.3) / 9  # 30% dari kalori untuk lemak (1g lemak = 9 kalori)
            user_fitness.hasil_hitungan_fat.value = round(fat_goal, 2)
            user_fitness.update()
        
        user_fitness.hasil_hitungan_fat = TextField(
            on_change=calculate_fat,
            label="Hasil Hitung Fat",
            hint_text="Hasil Hitungan Fat",
            read_only=True,
            suffix_text="kcal",  #Add the unit "kcal" to the text field
            expand=True
        )
        # Create a button to open
        user_fitness.hitung_fat_button = IconButton(
            icon=icons.CALCULATE_SHARP,
            icon_color=colors.BLUE_200,
            tooltip="Hitung Fat",
            on_click = calculate_fat,
        )

        
        user_fitness.inputanfitness_search = TextField(label="Search", hint_text="cari nama user ... ", expand=True, on_change=lambda e: tampil_data(e, search_query=e.control.value))
        user_fitness.snack_bar_save = SnackBar(Text("Data Fitness berhasil disimpan"), bgcolor="green")
        user_fitness.snack_bar_edit = SnackBar(Text("Data Fitness berhasil diedit"), bgcolor="orange")
        user_fitness.snack_bar_delete = SnackBar(Text("Data Fitness berhasil dihapus"), bgcolor="red")
        user_fitness.snack_bar_error = SnackBar(Text("Data Fitness ada yang error"), bgcolor="red")

        def tampil_data(e, search_query=""):
            # Merefresh halaman & menampilkan notif
            user_fitness.data_users_fitness.rows.clear()
            query = "SELECT * FROM users_fitness"
            if search_query:
                query += " WHERE user_name LIKE %s"
                cursor.execute(query, ("%" + search_query + "%",))
            else:
                cursor.execute(query)
            result = cursor.fetchall()

            # menampilkan ulang data
            if not result:
                user_fitness.data_users_fitness.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text("")),
                            DataCell(Text("Data not found")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text(""))
                        ]
                    )
                )
            else:
                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                for row in rows:
                    user_fitness.data_users_fitness.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(str(row['user_id']))),
                                DataCell(Text(row['user_name'])),
                                DataCell(Text(str(row['user_age']))),
                                DataCell(Text(str(row['user_training_date']))),
                                DataCell(Text(row['user_gender'])),
                                DataCell(Text(str(row['user_weight']))),
                                DataCell(Text(str(row['user_height']))),
                                DataCell(Text(row['user_activity_level'])),
                                DataCell(Text(str(row['user_calorie_goal']))),
                                DataCell(Text(str(row['user_protein_goal']))),
                                DataCell(Text(str(row['user_carb_goal']))),
                                DataCell(Text(str(row['user_fat_goal']))),
                                DataCell(
                                    Row([
                                        IconButton("delete", icon_color="red", data=row, on_click=hapus_users_fitness),
                                        IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                                    ])
                                ),
                            ]
                        )
                    )
            user_fitness.update()

        # fungsi menampilkan dialog form entri
        def tampil_dialog(e):
            user_fitness.inputan_user_id.value = ''
            user_fitness.inputan_user_name.value = ''
            user_fitness.inputan_user_age.value = ''
            user_fitness.inputan_training_date.value = ''
            user_fitness.inputan_user_gender.value = ''
            user_fitness.inputan_user_weight.value = ''
            user_fitness.inputan_user_height.value = ''
            user_fitness.inputan_user_activity_level.value = ''
            user_fitness.hasil_hitungan_kalori.value = ''
            user_fitness.hasil_hitungan_protein.value = ''
            user_fitness.hasil_hitungan_carb.value = ''
            user_fitness.hasil_hitungan_fat.value = ''
            user_fitness.dialog.open = True
            user_fitness.update()

        def tampil_dialog_ubah(e):
            user_fitness.inputan_user_id.value = e.control.data['user_id']
            user_fitness.inputan_user_name.value = e.control.data['user_name']
            user_fitness.inputan_user_age.value = e.control.data['user_age']
            user_fitness.inputan_training_date.value = e.control.data['user_training_date']
            user_fitness.inputan_user_gender.value = e.control.data['user_gender']
            user_fitness.inputan_user_weight.value = e.control.data['user_weight']
            user_fitness.inputan_user_height.value = e.control.data['user_height']
            user_fitness.inputan_user_activity_level.value = e.control.data['user_activity_level']
            user_fitness.hasil_hitungan_kalori.value = e.control.data['user_calorie_goal']
            user_fitness.hasil_hitungan_protein.value = e.control.data['user_protein_goal']
            user_fitness.hasil_hitungan_carb.value = e.control.data['user_carb_goal']
            user_fitness.hasil_hitungan_fat.value = e.control.data['user_fat_goal']
            user_fitness.dialog.open = True
            user_fitness.update()

        def simpan_user_fitness(e):
            try:
                # Prepare the SQL query and values based on whether it's an insert or update
                if user_fitness.inputan_user_id.value == '':
                    sql = """INSERT INTO users_fitness (user_name, user_age, user_training_date, user_gender, user_weight, user_height, user_activity_level, user_calorie_goal, user_protein_goal, user_carb_goal, user_fat_goal) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    val = (
                        user_fitness.inputan_user_name.value,
                        user_fitness.inputan_user_age.value,
                        user_fitness.inputan_training_date.value,
                        user_fitness.inputan_user_gender.value,
                        user_fitness.inputan_user_weight.value,
                        user_fitness.inputan_user_height.value,
                        user_fitness.inputan_user_activity_level.value,
                        user_fitness.hasil_hitungan_kalori.value,
                        user_fitness.hasil_hitungan_protein.value,
                        user_fitness.hasil_hitungan_carb.value,
                        user_fitness.hasil_hitungan_fat.value
                    )
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "Data di simpan!")
                    user_fitness.snack_bar_save.open = True
                else:
                    sql = """UPDATE users_fitness SET user_name = %s, user_age = %s, user_training_date = %s, user_gender = %s, user_weight = %s, user_height = %s, user_activity_level = %s, user_calorie_goal = %s, user_protein_goal = %s, user_carb_goal = %s, user_fat_goal = %s 
                            WHERE user_id = %s"""
                    val = (
                        user_fitness.inputan_user_name.value,
                        user_fitness.inputan_user_age.value,
                        user_fitness.inputan_training_date.value,
                        user_fitness.inputan_user_gender.value,
                        user_fitness.inputan_user_weight.value,
                        user_fitness.inputan_user_height.value,
                        user_fitness.inputan_user_activity_level.value,
                        user_fitness.hasil_hitungan_kalori.value,
                        user_fitness.hasil_hitungan_protein.value,
                        user_fitness.hasil_hitungan_carb.value,
                        user_fitness.hasil_hitungan_fat.value,
                        user_fitness.inputan_user_id.value
                    )
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "Data di update!")
                    user_fitness.snack_bar_edit.open = True
                

                tampil_data(e)
                user_fitness.dialog.open = False
                user_fitness.update()
            except Exception as ex:
                print(ex)
                print("Ada yang error!")
                user_fitness.snack_bar_error.open = True



        # fungsi hapus data
        def hapus_users_fitness(e):
            try:
                sql = "DELETE FROM users_fitness WHERE user_id = %s"
                val = (e.control.data['user_id'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                user_fitness.data_users_fitness.rows.clear()

                tampil_data(e)
                user_fitness.dialog.open = False
                user_fitness.snack_bar_delete.open = True
                user_fitness.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")
                user_fitness.snack_bar_error.open = True

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM users_fitness")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]
        user_fitness.data_users_fitness = DataTable(
            columns=[
            DataColumn(Text("User ID")),
            DataColumn(Text("Username")),
            DataColumn(Text("Age")),
            DataColumn(Text("Training Date")),
            DataColumn(Text("Gender")),
            DataColumn(Text("Weight")),
            DataColumn(Text("Height")),
            DataColumn(Text("Activity Level")),
            DataColumn(Text("Calorie Goal")),
            DataColumn(Text("Protein Goal")),
            DataColumn(Text("Carb Goal")),
            DataColumn(Text("Fat Goal")),
            DataColumn(Text("Options")),
            ],
        )
        for row in rows:
            user_fitness.data_users_fitness.rows.append(
            DataRow(
                cells=[
                DataCell(Text(str(row['user_id']))),
                DataCell(Text(row['user_name'])),
                DataCell(Text(str(row['user_age']))),
                DataCell(Text(str(row['user_training_date']))),
                DataCell(Text(row['user_gender'])),
                DataCell(Text(str(row['user_weight']))),
                DataCell(Text(str(row['user_height']))),
                DataCell(Text(row['user_activity_level'])),
                DataCell(Text(str(row['user_calorie_goal']))),
                DataCell(Text(str(row['user_protein_goal']))),
                DataCell(Text(str(row['user_carb_goal']))),
                DataCell(Text(str(row['user_fat_goal']))),
                DataCell(
                    Row([
                    IconButton("delete", icon_color="red", data=row, on_click=hapus_users_fitness),
                    IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                    ])
                ),
                ]
            )
            )
        cv = Column([user_fitness.data_users_fitness],scroll=True)
        rv = Row([cv],scroll=True,vertical_alignment=CrossAxisAlignment.START)
        
        # buat variabel utk layout data rekapan
        user_fitness.layout_data = Column()

        # buat form dialog untuk form entri data
        user_fitness.dialog = BottomSheet(
            Container(
            Column(
                [
                Text("Form Entri User Fitness", weight=FontWeight.BOLD),
                Row([user_fitness.inputan_user_id]),
                Row([user_fitness.inputan_user_name]),
                Row([user_fitness.inputan_user_age]),
                Row([user_fitness.inputan_training_date]),
                Row([user_fitness.tgl_lahir_button]),
                Row([user_fitness.inputan_user_gender]),
                Row([user_fitness.inputan_user_weight]),
                Row([user_fitness.inputan_user_height]),
                Row([user_fitness.inputan_user_activity_level]),
                Row([user_fitness.hasil_hitungan_kalori]),
                Row([user_fitness.hitung_kalori_button]),
                Row([user_fitness.hasil_hitungan_protein]),
                Row([user_fitness.hitung_protein_button]),
                Row([user_fitness.hasil_hitungan_carb]),
                Row([user_fitness.hitung_carb_button]),
                Row([user_fitness.hasil_hitungan_fat]),
                Row([user_fitness.hitung_fat_button]),
                Row([
                    # tombol tambah data
                    ElevatedButton(
                    "Simpan Data",
                    icon="SAVE_AS",
                    icon_color="white",
                    color="white",
                    bgcolor="teal",
                    width=280,
                    height=50,
                    on_click=simpan_user_fitness,
                    )
                ]),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                scroll=ScrollMode.ALWAYS,
                tight=True,
            ),
            padding=40,
            width=378,
            ),
            open=False,
            # on_dismiss=bs_dismissed,
        )

        return Column(
            controls=[
            Row([ElevatedButton("Tambah Data", icon=icons.ADD, icon_color="white", color="white", bgcolor="teal", on_click=tampil_dialog)], alignment=MainAxisAlignment.END),
            Row([user_fitness.inputanfitness_search]),
            user_fitness.dialog,
            user_fitness.snack_bar_save,
            user_fitness.snack_bar_edit,
            user_fitness.snack_bar_delete,
            user_fitness.snack_bar_error,
            rv,
            user_fitness.opsi_tanggal,
            ],
        )


class FormFood(UserControl):
    def build(food):

        # buat variabel inputan
        food.inputan_id_food = TextField(visible=False, expand=True)
        food.inputan_nama_food = TextField(label="Nama Makanan", hint_text="masukkan nama makanan ... ", expand=True)
        food.inputan_calories_food = TextField(label="Kalori", hint_text="masukkan jumlah kalori ... ", expand=True)
        food.inputan_protein_food = TextField(label="Protein", hint_text="masukkan jumlah protein ... ", expand=True)
        food.inputan_carbs_food = TextField(label="Karbohidrat", hint_text="masukkan jumlah karbohidrat ... ", expand=True)
        food.inputan_fat_food = TextField(label="Lemak", hint_text="masukkan jumlah lemak ... ", expand=True)
        food.inputan_diet_type_food = Dropdown(
            label="Tipe Diet",
            options=[
                dropdown.Option("Vegetarian"),
                dropdown.Option("Vegan"),
                dropdown.Option("Non-Vegetarian")
            ],
            expand=True
        )
        food.inputan_search = TextField(label="Search", hint_text="cari nama makanan ... ", expand=True, on_change=lambda e: tampil_data(e, search_query=e.control.value))
        food.snack_bar_save = SnackBar(Text("Data Foods berhasil disimpan"), bgcolor="green")
        food.snack_bar_edit = SnackBar(Text("Data Foods berhasil diedit"), bgcolor="orange")
        food.snack_bar_delete = SnackBar(Text("Data Foods berhasil dihapus"), bgcolor="red")
        food.snack_bar_error = SnackBar(Text("Data Foods ada yang error"), bgcolor="red")

        def tampil_data(e, search_query=""):
            # Merefresh halaman & menampilkan notif
            food.data_food.rows.clear()
            query = "SELECT * FROM foods"
            if search_query:
                query += " WHERE food_name LIKE %s"
                cursor.execute(query, ("%" + search_query + "%",))
            else:
                cursor.execute(query)
            result = cursor.fetchall()

            # menampilkan ulang data
            if not result:
                food.data_food.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text("")),
                            DataCell(Text("Data not found")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text(""))
                        ]
                    )
                )
            else:
                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                for row in rows:
                    food.data_food.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(row['food_id'])),
                                DataCell(Text(row['food_name'])),
                                DataCell(Text(row['food_calories'])),
                                DataCell(Text(row['food_protein'])),
                                DataCell(Text(row['food_carbs'])),
                                DataCell(Text(row['food_fat'])),
                                DataCell(Text(row['food_diet_type'])),
                                DataCell(
                                    Row([
                                        IconButton("delete", icon_color="red", data=row, on_click=hapus_food),
                                        IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                                    ])
                                ),
                            ]
                        )
                    )
            food.update()


        # fungsi menampilkan dialog form entri
        def tampil_dialog(e):
            food.inputan_id_food.value = ''
            food.inputan_nama_food.value = ''
            food.inputan_calories_food.value = ''
            food.inputan_protein_food.value = ''
            food.inputan_carbs_food.value = ''
            food.inputan_fat_food.value = ''
            food.inputan_diet_type_food.value = ''
            food.dialog.open = True
            food.update()

        def tampil_dialog_ubah(e):
            food.inputan_id_food.value = e.control.data['food_id']
            food.inputan_nama_food.value = e.control.data['food_name']
            food.inputan_calories_food.value = e.control.data['food_calories']
            food.inputan_protein_food.value = e.control.data['food_protein']
            food.inputan_carbs_food.value = e.control.data['food_carbs']
            food.inputan_fat_food.value = e.control.data['food_fat']
            food.inputan_diet_type_food.value = e.control.data['food_diet_type']
            food.dialog.open = True
            food.update()

        def simpan_food(e):
            try:
                if food.inputan_id_food.value == '':
                    sql = "INSERT INTO foods (food_name, food_calories, food_protein, food_carbs, food_fat, food_diet_type) VALUES(%s, %s, %s, %s, %s, %s)"
                    val = (food.inputan_nama_food.value, food.inputan_calories_food.value, food.inputan_protein_food.value, food.inputan_carbs_food.value, food.inputan_fat_food.value, food.inputan_diet_type_food.value)
                    
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "Data di simpan!")
                    
                    food.snack_bar_save.open = True
                else:
                    sql = "UPDATE foods SET food_name = %s, food_calories = %s, food_protein = %s, food_carbs = %s, food_fat = %s, food_diet_type = %s WHERE food_id = %s"
                    val = (food.inputan_nama_food.value, food.inputan_calories_food.value, food.inputan_protein_food.value, food.inputan_carbs_food.value, food.inputan_fat_food.value, food.inputan_diet_type_food.value, food.inputan_id_food.value)
                    
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "Data di update")
                    food.snack_bar_edit.open = True

                tampil_data(e)
                food.dialog.open = False
                food.update()
            except Exception as ex:
                print(ex)
                print("Ada yang error!")
                food.snack_bar_error.open = True


        def hapus_food(e):
            try:
                sql = "DELETE FROM foods WHERE food_id = %s"
                val = (e.control.data['food_id'],)
                with koneksi_db.cursor() as cursor:
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "data dihapus!")

                # Clear the rows and refresh data
                food.data_food.rows.clear()
                tampil_data(e)

                # Update UI elements
                food.dialog.open = False
                food.snack_bar_delete.open = True
                food.update()
            except Exception as ex:
                print(f"Error: {ex}")
                print("Ada yang error!")
                food.snack_bar_error.open = True

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM foods")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]
        food.data_food = DataTable(
            columns=[
                DataColumn(Text("ID")),
                DataColumn(Text("Nama Makanan")),
                DataColumn(Text("Kalori")),
                DataColumn(Text("Protein")),
                DataColumn(Text("Karbohidrat")),
                DataColumn(Text("Lemak")),
                DataColumn(Text("Tipe Diet")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            food.data_food.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row['food_id'])),
                        DataCell(Text(row['food_name'])),
                        DataCell(Text(row['food_calories'])),
                        DataCell(Text(row['food_protein'])),
                        DataCell(Text(row['food_carbs'])),
                        DataCell(Text(row['food_fat'])),
                        DataCell(Text(row['food_diet_type'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color="red", data=row, on_click=hapus_food),
                                IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                            ])
                        ),
                    ]
                )
            )
        cv = Column([food.data_food], scroll=True)
        rv = Row([cv], scroll=True, vertical_alignment=CrossAxisAlignment.START)

        # buat variabel utk layout data rekapan
        food.layout_data = Column()

        # buat form dialog untuk form entri data
        food.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Makanan", weight=FontWeight.BOLD),
                        Row([food.inputan_id_food]),
                        Row([food.inputan_nama_food]),
                        Row([food.inputan_calories_food]),
                        Row([food.inputan_protein_food]),
                        Row([food.inputan_carbs_food]),
                        Row([food.inputan_fat_food]),
                        Row([food.inputan_diet_type_food]),
                        Row([
                            # tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                icon="SAVE_AS",
                                icon_color="white",
                                color="white",
                                bgcolor="teal",
                                width=280,
                                height=50,
                                on_click=simpan_food,
                            )
                        ]),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll=ScrollMode.ALWAYS,
                    tight=True,
                ),
                padding=40,
                width=378
            ),
            open=False,
            # on_dismiss=bs_dismissed,
        )

        return Column(
            controls=[
                Row([ElevatedButton("Tambah Data", icon=icons.ADD, icon_color="white", color="white", bgcolor="teal", on_click=tampil_dialog)], alignment=MainAxisAlignment.END),
                Row([food.inputan_search]),
                rv, food.dialog, food.snack_bar_save, food.snack_bar_edit, food.snack_bar_delete, food.snack_bar_error
            ],
        )


class FormRecommendationFood(UserControl):
    def build(recommendfood):

        recommendfood.inputan_recommendation_foods_id = TextField(visible=False, expand=True)

        def get_food_ids():
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="fitness-calorie-center-bymth-db"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT food_id, food_name FROM foods")
                food_ids = cursor.fetchall()
                cursor.close()
                connection.close()
                return food_ids
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []

        def get_user_ids():
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="fitness-calorie-center-bymth-db"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT user_id, user_name FROM users_fitness")
                user_ids = cursor.fetchall()
                cursor.close()
                connection.close()
                return user_ids
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []

        def update_food_name_textfield(e):
            selected_food_id = e.control.value
            food_ids = get_food_ids()
            for food_id, food_name in food_ids:
                if str(food_id) == selected_food_id:
                    recommendfood.recommendfood_textfield_foodname.value = food_name
                    break
            recommendfood.update()

        def update_username_textfield(e):
            selected_user_id = e.control.value
            user_ids = get_user_ids()
            for user_id, user_name in user_ids:
                if str(user_id) == selected_user_id:
                    recommendfood.recommendfood_textfield_username.value = user_name
                    break
            recommendfood.update()

        recommendfood.recommend_food_id = Dropdown(
            label="Id Makanan",
            hint_text="Pilih Id makanan...",
            expand=True,
            options=[dropdown.Option(str(food_id), f"{food_id} - {food_name}") for food_id, food_name in get_food_ids()],
            on_change=update_food_name_textfield
        )

        recommendfood.recommendfood_textfield_foodname = TextField(
            label="Nama Makanan",
            hint_text="Nama Makanan...",
            expand=True,
            read_only=True
        )

        recommendfood.recommend_user_id = Dropdown(
            label="Id User",
            hint_text="Pilih Id User...",
            expand=True,
            options=[dropdown.Option(str(user_id), f"{user_id} - {user_name}") for user_id, user_name in get_user_ids()],
            on_change=update_username_textfield
        )

        recommendfood.recommendfood_textfield_username = TextField(
            label="Username",
            hint_text="Username...",
            expand=True,
            read_only=True
        )

        recommendfood.inputan_recommendation_date = TextField(label="Recommendation Date", read_only=True)

        def ubah_tanggal(e):
            tgl_baru = recommendfood.opsi_tanggal.value
            recommendfood.inputan_recommendation_date.value = str(tgl_baru)
            recommendfood.update()

        def opsi_tanggal_dismissed(e):
            recommendfood.update()

        recommendfood.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal,
            on_dismiss=opsi_tanggal_dismissed,
            first_date=datetime.datetime(1945, 1, 1),
            last_date=datetime.date.today(),
        )

        recommendfood.recommend_food_date_button = IconButton(
            icon=icons.DATE_RANGE_OUTLINED,
            icon_color=colors.GREEN,
            tooltip="Pilih Tanggal",
            on_click=lambda _: recommendfood.opsi_tanggal.pick_date(),
        )

        recommendfood.inputanrecommendfood_search = TextField(label="Search", hint_text="cari nama makanan ... ", expand=True, on_change=lambda e: tampil_data(e, search_query=e.control.value))
        recommendfood.snack_bar_save = SnackBar(Text("Data Recommend Foods berhasil disimpan"), bgcolor="green")
        recommendfood.snack_bar_edit = SnackBar(Text("Data Recommend Foods berhasil diedit"), bgcolor="orange")
        recommendfood.snack_bar_delete = SnackBar(Text("Data Recommend Foods berhasil dihapus"), bgcolor="red")
        recommendfood.snack_bar_error = SnackBar(Text("Data Recommend Foods ada yang error"), bgcolor="red")

        def tampil_data(e, search_query=""):
            # Merefresh halaman & menampilkan notif
            recommendfood.data_recommend_food.rows.clear()
            query = "SELECT * FROM food_recommendations"
            if search_query:
                query += " WHERE food_name LIKE %s"
                cursor.execute(query, ("%" + search_query + "%",))
            else:
                cursor.execute(query)
            result = cursor.fetchall()

            # menampilkan ulang data
            if not result:
                recommendfood.data_recommend_food.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("")),
                            DataCell(Text("Data not found")),
                            DataCell(Text("")),
                            DataCell(Text(""))
                        ]
                    )
                )
            else:
                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                for row in rows:
                    recommendfood.data_recommend_food.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(row['recommendation_id'])),
                                DataCell(Text(row['user_id'])),
                                DataCell(Text(row['food_id'])),
                                DataCell(Text(row['user_name'])),
                                DataCell(Text(row['food_name'])),
                                DataCell(Text(row['recommendation_date'])),
                                DataCell(
                                    Row([
                                        IconButton("delete", icon_color="red", data=row, on_click=hapus_recommend_food),
                                        IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                                    ])
                                ),
                            ]
                        )
                    )
            recommendfood.update()


        def tampil_dialog(e):
            recommendfood.inputan_recommendation_foods_id.value = ''
            recommendfood.recommend_food_id.value = ''
            recommendfood.recommendfood_textfield_foodname.value = ''
            recommendfood.recommend_user_id.value = ''
            recommendfood.recommendfood_textfield_username.value = ''
            recommendfood.inputan_recommendation_date.value = ''
            recommendfood.opsi_tanggal.value = None
            recommendfood.dialog.open = True
            recommendfood.update()

        def tampil_dialog_ubah(e):
            recommendfood.inputan_recommendation_foods_id.value = e.control.data['recommendation_id']
            recommendfood.recommend_food_id.value = e.control.data['food_id']
            recommendfood.recommendfood_textfield_foodname.value = e.control.data['food_name']
            recommendfood.recommend_user_id.value = e.control.data['user_id']
            recommendfood.recommendfood_textfield_username.value = e.control.data['user_name']
            recommendfood.inputan_recommendation_date.value = e.control.data['recommendation_date']
            recommendfood.opsi_tanggal.value = e.control.data['recommendation_date']
            recommendfood.dialog.open = True
            recommendfood.update()

        def simpan_recommend_food(e):
            try:
                if recommendfood.recommend_food_id.value == '' or recommendfood.recommend_user_id.value == '':
                    print("User ID dan Food ID tidak boleh kosong!")
                    recommendfood.snack_bar_error.open = True
                    recommendfood.snack_bar_error.text = "User ID and Food ID cannot be empty!"
                    return

                if recommendfood.inputan_recommendation_foods_id.value == '':
                    # Insert new record
                    sql = "INSERT INTO food_recommendations (user_id, food_id, user_name, food_name, recommendation_date) VALUES (%s, %s, %s, %s, %s)"
                    val = (
                        recommendfood.recommend_user_id.value,
                        recommendfood.recommend_food_id.value,
                        recommendfood.recommendfood_textfield_username.value,
                        recommendfood.recommendfood_textfield_foodname.value,
                        recommendfood.inputan_recommendation_date.value
                    )
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "Data berhasil disimpan!")

                    recommendfood.snack_bar_save.open = True
                else:
                    # Update existing record
                    sql = "UPDATE food_recommendations SET user_id = %s, food_id = %s, user_name = %s, food_name = %s, recommendation_date = %s WHERE recommendation_id = %s"
                    val = (
                        recommendfood.recommend_user_id.value,
                        recommendfood.recommend_food_id.value,
                        recommendfood.recommendfood_textfield_username.value,
                        recommendfood.recommendfood_textfield_foodname.value,
                        recommendfood.inputan_recommendation_date.value,
                        recommendfood.inputan_recommendation_foods_id.value
                    )
                    cursor.execute(sql, val)
                    koneksi_db.commit()
                    print(cursor.rowcount, "Data berhasil disimpan!")

                    recommendfood.snack_bar_edit.open = True

                tampil_data(e)
                recommendfood.dialog.open = False
                recommendfood.update()
            except Exception as ex:
                print(ex)
                print("Ada yang error!")
                recommendfood.snack_bar_error.open = True



        def hapus_recommend_food(e):
            try:
                sql = "DELETE FROM food_recommendations WHERE recommendation_id = %s"
                val = (e.control.data['recommendation_id'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                recommendfood.data_recommend_food.rows.clear()
                
                tampil_data(e)
                recommendfood.dialog.open = False
                recommendfood.snack_bar_delete.open = True
                recommendfood.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")
                recommendfood.snack_bar_error.open = True

        cursor.execute("SELECT * FROM food_recommendations")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]
        recommendfood.data_recommend_food = DataTable(
            columns=[
                DataColumn(Text("Recommend ID")),
                DataColumn(Text("User Id")),
                DataColumn(Text("Food Id")),
                DataColumn(Text("User Name")),
                DataColumn(Text("Food Name")),
                DataColumn(Text("Recommendation Date")),
                DataColumn(Text("Opsi")),
            ],
        )

        for row in rows:
            recommendfood.data_recommend_food.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row['recommendation_id'])),
                        DataCell(Text(row['user_id'])),
                        DataCell(Text(row['food_id'])),
                        DataCell(Text(row['user_name'])),
                        DataCell(Text(row['food_name'])),
                        DataCell(Text(row['recommendation_date'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color="red", data=row, on_click=hapus_recommend_food),
                                IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                            ])
                        ),
                    ]
                )
            )
        cv = Column([recommendfood.data_recommend_food],scroll=True)
        rv = Row([cv],scroll=True,vertical_alignment=CrossAxisAlignment.START)

        recommendfood.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Formulir Recommendation", weight=FontWeight.BOLD, size=20),
                        Row([recommendfood.inputan_recommendation_foods_id]),
                        Row([recommendfood.recommend_food_id]),
                        Row([recommendfood.recommendfood_textfield_foodname]),
                        Row([recommendfood.recommend_user_id]),
                        Row([recommendfood.recommendfood_textfield_username]),
                        Row([recommendfood.inputan_recommendation_date]),
                        Row([recommendfood.recommend_food_date_button]),
                        Row([
                        #tombol tambah data
                        ElevatedButton(
                        "Simpan Data",
                            icon = "SAVE_AS",
                            icon_color = "white",
                            color = "white",
                            bgcolor = "teal",
                            width = 280,
                            height = 50,
                            on_click = simpan_recommend_food,
                        )
                    ]),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    tight=True,
                    # alignment=MainAxisAlignment.CENTER,
                    scroll=ScrollMode.ALWAYS
                ),
                padding=20,
                border_radius=10,
            ),
            open=False,
        )

        return Column(
            width=800,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text("Recommendation Food", weight=FontWeight.BOLD, size=20),
                ElevatedButton("Tambah Data", icon=icons.ADD, icon_color="white", color="white", bgcolor="teal", on_click=tampil_dialog),
                Row([recommendfood.inputanrecommendfood_search]),
                rv,
                recommendfood.opsi_tanggal,
                recommendfood.dialog,
                recommendfood.snack_bar_save, recommendfood.snack_bar_edit, recommendfood.snack_bar_delete, recommendfood.snack_bar_error
            ],
        )

class FormShowRF(UserControl):
    def build(showrecommendfood):

        def get_user_ids():
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="fitness-calorie-center-bymth-db"
                )
                cursor = connection.cursor()
                cursor.execute("SELECT user_id, user_name FROM users_fitness")
                user_ids = cursor.fetchall()
                cursor.close()
                connection.close()
                return user_ids
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []

        def update_username_textfield(e):
            selected_user_id = e.control.value
            user_ids = get_user_ids()
            for user_id, user_name in user_ids:
                if str(user_id) == selected_user_id:
                    showrecommendfood.recommendfood_textfield_username.value = user_name
                    break
            showrecommendfood.update()

        def get_user_recommendations(user_id):
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="fitness-calorie-center-bymth-db"
                )
                cursor = connection.cursor()
                sql = """
                    SELECT 
                        f.food_name, 
                        f.food_calories, 
                        f.food_protein, 
                        f.food_carbs, 
                        f.food_fat, 
                        f.food_diet_type
                    FROM 
                        foods f
                    JOIN 
                        users_fitness u ON u.user_id = %s
                    WHERE 
                        f.food_calories <= u.user_calorie_goal
                        AND (f.food_diet_type = 'Vegan' OR f.food_diet_type = 'Vegetarian' OR f.food_diet_type = 'Non-Vegetarian');
                """
                cursor.execute(sql, (user_id,))
                recommendations = cursor.fetchall()
                cursor.close()
                connection.close()
                return recommendations
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return []

        def display_recommendations(e):
            user_id = showrecommendfood.recommend_user_id.value
            recommendations = get_user_recommendations(user_id)
            showrecommendfood.recommendation_cards.controls.clear()

            if recommendations:
                for rec in recommendations:
                    food_name, calories, protein, carbs, fat, diet_type = rec
                    card = Card(
                        content=Column([
                            Text(f"Food Name: {food_name}", size=16, weight="bold"),
                            Text(f"Calories: {calories}", size=14),
                            Text(f"Protein: {protein}", size=14),
                            Text(f"Carbs: {carbs}", size=14),
                            Text(f"Fat: {fat}", size=14),
                            Text(f"Diet Type: {diet_type}", size=14),
                        ], spacing=10)
                    )
                    showrecommendfood.recommendation_cards.controls.append(card)
            else:
                showrecommendfood.recommendation_cards.controls.append(Text("No recommendations found."))

            showrecommendfood.update()

        showrecommendfood.recommend_user_id = Dropdown(
            label="Id User",
            hint_text="Pilih Id User...",
            expand=True,
            options=[dropdown.Option(str(user_id), f"{user_id} - {user_name}") for user_id, user_name in get_user_ids()],
            on_change=update_username_textfield
        )

        showrecommendfood.recommendfood_textfield_username = TextField(
            label="Username",
            hint_text="Username...",
            expand=True,
            read_only=True
        )

        showrecommendfood.recommendation_cards = Column()

        showrecommendfood.refresh_button = ElevatedButton(
            text="Show Recommendations",
            icon=icons.LIST_ALT_ROUNDED, icon_color="white", color="white", bgcolor="teal",
            on_click=display_recommendations
        )

        return Container(
            content=Column([
                Container(
                    content=Row([
                        showrecommendfood.recommend_user_id,
                        showrecommendfood.recommendfood_textfield_username
                    ], spacing=20),
                    padding=padding.symmetric(vertical=10)
                ),
                showrecommendfood.refresh_button,
                Divider(height=20, thickness=1),
                showrecommendfood.recommendation_cards
            ], spacing=20),
            padding=padding.all(20)
        )

# Fungsi koneksi database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="fitness-calorie-center-bymth-db"
    )

# Fungsi utama untuk menjalankan aplikasi
def main(page: Page):
    # Configure the page
    page.title = "Aplikasi CRUD FITNESS FOOD"
    page.window_width = 375
    page.window_height = 750
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.scroll = "adaptive"
    page.theme_mode = ThemeMode.LIGHT  # Set initial mode to light

    tab_titles = [
        "Aplikasi FitnessFood",
        "Data Fitness",
        "Data Foods",
        "FitFood Recommend",
        "Settings"
    ]

    # Fungsi untuk toggle dark/light mode
    def mode_tema(e):
        page.theme_mode = ThemeMode.LIGHT if page.theme_mode == ThemeMode.DARK else ThemeMode.DARK
        update_ui()
        page.update()

    # Fetch data for summary cards from the database
    def fetch_summary_data():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM food_recommendations")
        total_workouts = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(food_calories) FROM foods")
        calories_burned = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(user_activity_level) FROM users_fitness")
        active_minutes = cursor.fetchone()[0]

        cursor.close()
        db.close()
        return total_workouts, calories_burned, active_minutes

    # Fungsi untuk membuat kartu rangkuman
    def create_summary_card(icon, title, value, dark_mode):
        return Card(
            content=Container(
                content=Column(
                    [
                        Icon(icon, size=40, color=colors.ORANGE if not dark_mode else colors.YELLOW),
                        Text(title, size=16, weight="bold", color=colors.BLACK if not dark_mode else colors.WHITE),
                        Text(str(value), size=24, weight="bold", color=colors.BLACK if not dark_mode else colors.WHITE),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                padding=padding.only(top=3, bottom=10),
                bgcolor=colors.AMBER_50 if not dark_mode else colors.AMBER_900,
                border_radius=10,
            ),
            width=150,
            elevation=5,
        )

    # Fungsi untuk membangun layout kartu rangkuman
    def build_summary_cards_layout(dark_mode):
        total_workouts, calories_burned, active_minutes = fetch_summary_data()

        if page.window_width < 600 or page.window_height < 800:
            return Column(
                controls=[
                    create_summary_card(icons.FITNESS_CENTER, "Total Workouts", total_workouts, dark_mode),
                    create_summary_card(icons.CALCULATE_ROUNDED, "Calories Burned", calories_burned, dark_mode),
                    create_summary_card(icons.AV_TIMER, "Total Activity", active_minutes, dark_mode),
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=20,
            )
        else:
            return Row(
                controls=[
                    create_summary_card(icons.FITNESS_CENTER, "Total Workouts", total_workouts, dark_mode),
                    create_summary_card(icons.CALCULATE_ROUNDED, "Calories Burned", calories_burned, dark_mode),
                    create_summary_card(icons.AV_TIMER, "Active Minutes", active_minutes, dark_mode),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                spacing=20,
            )

    # Pie chart creation
    normal_radius = 100
    hover_radius = 110
    normal_title_style = TextStyle(size=12, color=colors.WHITE, weight=FontWeight.BOLD)
    hover_title_style = TextStyle(
        size=16, color=colors.WHITE, weight=FontWeight.BOLD, shadow=BoxShadow(blur_radius=2, color=colors.BLACK54)
    )
    normal_badge_size = 40
    hover_badge_size = 50

    chart = PieChart(
        sections=[],
        sections_space=0,
        center_space_radius=0,
        expand=True,
    )

    # Badge creation function
    def badge(icon, size):
        return Container(
            content=Icon(icon),
            width=size,
            height=size,
            border=border.all(1, colors.BROWN),
            border_radius=size / 2,
            bgcolor=colors.WHITE,
        )

    # Event handling for pie chart
    def on_chart_event(e):
        if chart._Control__page:  # Ensure chart has been added to page
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            chart.update()

    chart.on_chart_event = on_chart_event

    # Fetch food recommendations from the database
    def get_food_recommendations():
        db = connect_db()
        cursor = db.cursor()
        query = """
        SELECT foods.food_name, COUNT(*) as count
        FROM food_recommendations
        JOIN foods ON food_recommendations.food_id = foods.food_id
        GROUP BY foods.food_name
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return results

    # Predefined list of colors
    color_list = [
        colors.BLUE, colors.RED, colors.GREEN, colors.YELLOW, colors.PURPLE, colors.ORANGE, colors.PINK, colors.BROWN
    ]

    # Update pie chart with data
    def update_pie_chart():
        recommendations = get_food_recommendations()
        chart.sections = [
            PieChartSection(
                value=count,
                title=f"{food_name} ({count})",
                title_style=normal_title_style,
                color=color_list[i % len(color_list)],  # Assign color in round-robin fashion
                radius=normal_radius,
                badge=badge(icons.FOOD_BANK_ROUNDED, normal_badge_size),  # Customize icon as needed
                badge_position=0.98,
            ) for i, (food_name, count) in enumerate(recommendations)
        ]
        if chart._Control__page:  # Ensure chart has been added to page
            chart.update()

    # Fungsi untuk membuat tampilan utama
    def create_main_view(dark_mode):
        # Create main view container
        main_view = Column(
            controls=[
                Row(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(
                                        content=Text(
                                            "Dashboard Home",
                                            size=20,
                                            weight="bold",
                                            color=colors.BLACK if not dark_mode else colors.WHITE,
                                        ),
                                        alignment=alignment.top_left,
                                    ),
                                    build_summary_cards_layout(dark_mode),
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            height=550,
                            width=350,
                        ),
                    ],
                ),
                Row(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(
                                        content=Text("Analisis Aktivitas FitnessFood", size=20, weight="bold", color=colors.BLACK if not dark_mode else colors.WHITE),
                                        alignment=alignment.top_left,
                                    ),
                                    chart,
                                    Text('FitnessFood APP @2024', size=12, color=colors.BLACK if not dark_mode else colors.WHITE)
                                ],
                                alignment=MainAxisAlignment.SPACE_AROUND,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            height=350,
                            width=350,
                        ),
                    ],
                ),
            ],
            alignment=MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        return main_view

    # Data Fitness view creation
    def create_data_fitness_view():
        return Column(
            controls=[
                Text("Data Fitness Page Content"),
                FormUserFitness()
            ]
        )

    # Foods view creation
    def create_foods_view():
        return Column(
            controls=[
                Text("Data Foods Page Content"),
                FormFood(),
            ]
        )

    # Fitness Recommendation view creation
    def create_fitness_recommendation_view():
        return Column(
            controls=[
                Text("Fitness Food Recommendation Page Content"),
                FormRecommendationFood(),
                FormShowRF(),
            ]
        )

    # Settings view creation
    def create_settings_view():
        return Column(
            controls=[
                Text("Settings Page", size=30, weight="bold"),
                Text("Selamat datang di Fitness Food: Sistem Rekomendasi Nutrisi dan Makanan Pribadi"),
                Text("Aplikasi ini membantu Anda mengelola nutrisi dan mendapatkan rekomendasi makanan yang dipersonalisasi."),
                Text("User Fitness", size=20, weight="bold"),
                Text("Halaman ini membantu aplikasi Fitness Food dalam mengelola dan mengakses informasi tentang setiap pengguna, sehingga dapat memberikan rekomendasi makanan yang sesuai dengan kebutuhan gizi dan preferensi makanan setiap pengguna."),
                Text("Nutrition Food Preferences", size=20, weight="bold"),
                Text("Halaman ini membantu aplikasi Fitness Food dalam mengelola dan mengakses informasi tentang setiap makanan yang tersedia, sehingga dapat memberikan rekomendasi makanan yang sesuai dengan kebutuhan gizi dan preferensi makanan setiap pengguna."),
                Text("Food Recommendations", size=20, weight="bold"),
                Text("Halaman ini membantu aplikasi Fitness Food dalam merekam dan mengelola rekomendasi makanan yang diberikan kepada setiap pengguna."),
            ]
        )

    # Change tab function
    def change_tab(e):
        selected_index = e.control.selected_index
        tab_1.visible = selected_index == 0
        tab_2.visible = selected_index == 1
        tab_3.visible = selected_index == 2
        tab_4.visible = selected_index == 3
        tab_5.visible = selected_index == 4
        update_ui()
        page.update()

    # Set AppBar
    def set_appbar(dark_mode):
        page.appbar = AppBar(
            title=Row(
                controls=[
                    Container(width=5),  # Adjust the width as necessary
                    Text(
                        tab_titles[page.navigation_bar.selected_index],
                        size=24,
                        weight="bold",
                        color=colors.BLACK if not dark_mode else colors.WHITE,
                    ),
                    # Container(width=5),  # Adjust the width as necessary
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
            bgcolor=colors.ORANGE,
            actions=[
                IconButton(icons.WB_SUNNY_OUTLINED, on_click=mode_tema),
            ],
        )


    # Fungsi untuk memperbarui UI berdasarkan mode tema
    def update_ui():
        dark_mode = page.theme_mode == ThemeMode.DARK
        # Update AppBar
        set_appbar(dark_mode)
        # Update main view
        tab_1.content = create_main_view(dark_mode)
        page.update()  # Update the page after changing the main view content
        update_pie_chart()  # Update pie chart after the main view content is updated

        # Update the tab title colors
        for i, _ in enumerate(tab_titles):
            if i == page.navigation_bar.selected_index:
                page.navigation_bar.destinations[i].icon_color = colors.WHITE if not dark_mode else colors.BLACK
                page.navigation_bar.destinations[i].label_color = colors.WHITE if not dark_mode else colors.BLACK
            else:
                page.navigation_bar.destinations[i].icon_color = colors.BLUE_900 if not dark_mode else colors.GREY
                page.navigation_bar.destinations[i].label_color = colors.BLUE_900 if not dark_mode else colors.GREY

    # Create tabs
    tab_1 = Container(visible=True)
    tab_2 = Container(content=create_data_fitness_view(), visible=False)
    tab_3 = Container(content=create_foods_view(), visible=False)
    tab_4 = Container(content=create_fitness_recommendation_view(), visible=False)
    tab_5 = Container(content=create_settings_view(), visible=False)

    # Add tabs to page
    page.add(
        Column(controls=[
            tab_1,
            tab_2,
            tab_3,
            tab_4,
            tab_5,
        ])
    )

    # Set navigation bar
    page.navigation_bar = CupertinoNavigationBar(
        bgcolor=colors.ORANGE,
        inactive_color=colors.BLUE_900,
        active_color=colors.WHITE,
        on_change=change_tab,
        selected_index=0,
        destinations=[
            NavigationDestination(icon=icons.HOME, label="Home"),
            NavigationDestination(icon=icons.DATA_USAGE, label="User Fit"),
            NavigationDestination(icon=icons.FOOD_BANK, label="Foods"),
            NavigationDestination(icon=icons.RECOMMEND, label="Recommenfood"),
            NavigationDestination(icon=icons.SETTINGS, label="Settings"),
        ],
    )

    # Call update_ui after the page is set up
    update_ui()
    update_pie_chart()
    page.update()
    

# Mengatur output aplikasi
flet.app(target=main)
