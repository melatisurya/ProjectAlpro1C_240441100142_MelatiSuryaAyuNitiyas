import os
import time
import datetime

class User:
    def _init_(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Camera:
    def _init_(self, id, name, brand, daily_rate):
        self.id = id
        self.name = name
        self.brand = brand
        self.daily_rate = daily_rate

class RentalSystem:
    def _init_(self):
        self.users = []
        self.cameras = []
        self.rentals = []
        self.returned_rentals = []
        self.admin_username = "admin"
        self.admin_password = "admin123"
        self.initialize_default_cameras()

    def initialize_default_cameras(self):
        default_cameras = [
            Camera(1, "Canon EOS R5", "Canon", 250000),
            Camera(2, "Sony A7 III", "Sony", 200000),
            Camera(3, "Nikon Z6", "Nikon", 180000)
        ]
        self.cameras.extend(default_cameras)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self, title):
        print("\n" + "="*50)
        print(title.center(50))
        print("="*50)

    def input_with_validation(self, prompt):
        while True:
            value = input(prompt)
            if value.strip():
                return value
            print("Input tidak boleh kosong!")

    def register_user(self):
        self.header("REGISTRASI PENGGUNA")
        while True:
            user_id = self.input_with_validation("Masukkan ID Pengguna: ")
            
            # Cek apakah ID sudah ada
            if any(user.id == user_id for user in self.users):
                print("ID sudah digunakan. Silakan gunakan ID lain.")
                continue

            username = self.input_with_validation("Masukkan Username: ")
            password = self.input_with_validation("Masukkan Password: ")

            new_user = User(user_id, username, password)
            self.users.append(new_user)
            print("\nRegistrasi berhasil!")
            time.sleep(1)
            break

    def user_login(self):
        self.header("LOGIN PENGGUNA")
        username = self.input_with_validation("Username: ")
        password = self.input_with_validation("Password: ")

        for user in self.users:
            if user.username == username and user.password == password:
                return user
        
        print("Login gagal. Username atau password salah.")
        time.sleep(1)
        return None

    def admin_login(self):
        self.header("LOGIN ADMIN")
        username = self.input_with_validation("Username Admin: ")
        password = self.input_with_validation("Password Admin: ")

        if username == self.admin_username and password == self.admin_password:
            return True
        
        print("Login admin gagal.")
        time.sleep(1)
        return False

    def display_cameras(self):
        self.header("DAFTAR KAMERA")
        print("{:<5} {:<20} {:<15} {:<10}".format("ID", "Nama Kamera", "Merk", "Harga/Hari"))
        print("-"*50)
        for camera in self.cameras:
            print("{:<5} {:<20} {:<15} Rp{:,}".format(
                camera.id, camera.name, camera.brand, camera.daily_rate
            ))

    def rent_camera(self, user):
        self.display_cameras()
        camera_id = int(self.input_with_validation("Pilih ID Kamera: "))
        days = int(self.input_with_validation("Berapa hari ingin disewa: "))

        camera = next((c for c in self.cameras if c.id == camera_id), None)
        if camera:
            total_cost = camera.daily_rate * days
            rental_info = {
                'user_id': user.id,
                'camera_name': camera.name,
                'days': days,
                'total_cost': total_cost,
                'rental_date': datetime.datetime.now()
            }
            self.rentals.append(rental_info)
            self.print_rental_receipt(rental_info)
        else:
            print("Kamera tidak ditemukan.")

    def print_rental_receipt(self, rental):
        self.header("STRUK PENYEWAAN KAMERA")
        print(f"ID Pengguna: {rental['user_id']}")
        print(f"Nama Kamera: {rental['camera_name']}")
        print(f"Lama Sewa: {rental['days']} hari")
        print(f"Total Biaya: Rp{rental['total_cost']:,}")
        print(f"Tanggal Sewa: {rental['rental_date'].strftime('%Y-%m-%d %H:%M:%S')}")
        input("\nTekan Enter untuk melanjutkan...")

    def update_camera_price(self):
        self.display_cameras()
        camera_id = int(self.input_with_validation("Pilih ID Kamera untuk diperbarui harganya: "))
        
        camera = next((c for c in self.cameras if c.id == camera_id), None)
        if camera:
            new_price = int(self.input_with_validation("Masukkan harga baru per hari: "))
            camera.daily_rate = new_price
            print("Harga berhasil diperbarui!")
        else:
            print("Kamera tidak ditemukan.")

    def view_rental_history(self, user):
        self.header(f"RIWAYAT PENYEWAAN {user.username}")
        user_rentals = [rental for rental in self.rentals if rental['user_id'] == user.id]
        
        if not user_rentals:
            print("Belum ada riwayat penyewaan.")
            input("Tekan Enter untuk kembali...")
            return

        print("{:<15} {:<20} {:<10} {:<15} {:<15}".format(
            "ID Kamera", "Nama Kamera", "Lama Sewa", "Harga Satuan", "Total Biaya"
        ))
        print("-"*70)
        
        for rental in user_rentals:
            camera = next((c for c in self.cameras if c.name == rental['camera_name']), None)
            print("{:<15} {:<20} {:<10} Rp{:,} Rp{:,}".format(
                camera.id if camera else "N/A", 
                rental['camera_name'], 
                f"{rental['days']} hari", 
                camera.daily_rate if camera else 0,
                rental['total_cost']
            ))
        
        input("\nTekan Enter untuk kembali...")

    def return_camera(self, user):
        user_active_rentals = [rental for rental in self.rentals if rental['user_id'] == user.id]
        
        if not user_active_rentals:
            print("Anda tidak memiliki kamera yang sedang disewa.")
            input("Tekan Enter untuk kembali...")
            return

        self.header("PENGEMBALIAN KAMERA")
        print("{:<5} {:<20} {:<15} {:<15}".format("No", "Nama Kamera", "Lama Sewa", "Total Biaya"))
        print("-"*55)

        for i, rental in enumerate(user_active_rentals, 1):
            print("{:<5} {:<20} {:<15} Rp{:,}".format(
                i, rental['camera_name'], f"{rental['days']} hari", rental['total_cost']
            ))

        choice = int(self.input_with_validation("Pilih nomor kamera yang akan dikembalikan: "))
        
        if 1 <= choice <= len(user_active_rentals):
            returned_rental = user_active_rentals[choice - 1]
            
            konfirmasi = input("Apakah Anda yakin ingin mengembalikan kamera? (y/n): ").lower()
            if konfirmasi == 'y':
                returned_rental['return_date'] = datetime.datetime.now()
                self.returned_rentals.append(returned_rental)
                self.rentals.remove(returned_rental)
                self.print_return_receipt(returned_rental)
            else:
                print("Pengembalian dibatalkan.")
        else:
            print("Pilihan tidak valid.")

    def print_return_receipt(self, rental):
        self.header("STRUK PENGEMBALIAN KAMERA")
        print(f"ID Pengguna: {rental['user_id']}")
        print(f"Nama Kamera: {rental['camera_name']}")
        print(f"Lama Sewa: {rental['days']} hari")
        print(f"Total Biaya: Rp{rental['total_cost']:,}")
        print(f"Tanggal Sewa: {rental['rental_date'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tanggal Kembali: {rental['return_date'].strftime('%Y-%m-%d %H:%M:%S')}")
        input("\nTekan Enter untuk melanjutkan...")

    def view_all_rentals(self):
        self.header("RIWAYAT PENYEWAAN")
        if not self.rentals:
            print("Belum ada riwayat penyewaan.")
            input("Tekan Enter untuk kembali...")
            return

        print("{:<15} {:<20} {:<10} {:<15} {:<20}".format(
            "ID Pengguna", "Nama Kamera", "Lama Sewa", "Total Biaya", "Tanggal Sewa"
        ))
        print("-" * 80)
        
        for rental in self.rentals:
            print("{:<15} {:<20} {:<10} Rp{:,} {}".format(
                rental['user_id'],
                rental['camera_name'],
                f"{rental['days']} hari",
                rental['total_cost'],
                rental['rental_date'].strftime('%Y-%m-%d %H:%M:%S')
            ))
        input("\nTekan Enter untuk kembali...")

    def view_all_returns(self):
        self.header("RIWAYAT PENGEMBALIAN")
        if not self.returned_rentals:
            print("Belum ada riwayat pengembalian.")
            input("Tekan Enter untuk kembali...")
            return

        print("{:<15} {:<20} {:<10} {:<15} {:<20}".format(
            "ID Pengguna", "Nama Kamera", "Lama Sewa", "Total Biaya", "Tanggal Pengembalian"
        ))
        print("-" * 80)
        
        for rental in self.returned_rentals:
            print("{:<15} {:<20} {:<10} Rp{:,} {}".format(
                rental['user_id'],
                rental['camera_name'],
                f"{rental['days']} hari",
                rental['total_cost'],
                rental['return_date'].strftime('%Y-%m-%d %H:%M:%S')
            ))
        input("\nTekan Enter untuk kembali...")

    def admin_menu(self):
        while True:
            self.clear_screen()
            self.header("MENU ADMIN")
            print("1. Lihat Daftar Kamera")
            print("2. Perbarui Harga Kamera")
            print("3. Lihat Riwayat Penyewaan")
            print("4. Lihat Riwayat Pengembalian")
            print("5. Kembali")

            choice = self.input_with_validation("Pilih menu: ")

            if choice == '1':
                self.display_cameras()
                input("Tekan Enter untuk kembali...")
            elif choice == '2':
                self.update_camera_price()
            elif choice == '3':
                self.view_all_rentals()
            elif choice == '4':
                self.view_all_returns()
            elif choice == '5':
                break
            else:
                print("Pilihan tidak valid.")
                time.sleep(1)

    def user_menu(self, user):
        while True:
            self.clear_screen()
            self.header("MENU PENGGUNA")
            print("1. Lihat Daftar Kamera")
            print("2. Sewa Kamera")
            print("3. Lihat Riwayat Penyewaan")
            print("4. Kembalikan Kamera")
            print("5. Logout")

            choice = self.input_with_validation("Pilih menu: ")

            if choice == '1':
                self.display_cameras()
                input("Tekan Enter untuk kembali...")
            elif choice == '2':
                self.rent_camera(user)
            elif choice == '3':
                self.view_rental_history(user)
            elif choice == '4':
                self.return_camera(user)
            elif choice == '5':
                break
            else:
                print("Pilihan tidak valid.")
                time.sleep(1)

    def run(self):
        while True:
            self.clear_screen()
            self.header("SISTEM RENTAL KAMERA")
            print("1. Login Pengguna")
            print("2. Login Admin")
            print("3. Registrasi Pengguna")
            print("4. Keluar")

            choice = self.input_with_validation("Pilih menu: ")

            if choice == '1':
                user = self.user_login()
                if user:
                    self.user_menu(user)
            elif choice == '2':
                if self.admin_login():
                    self.admin_menu()
            elif choice == '3':
                self.register_user()
            elif choice == '4':
                print("Terima kasih telah menggunakan sistem rental kamera!")
                break
            else:
                print("Pilihan tidak valid.")
                time.sleep(1)

system = RentalSystem()
system.run()
