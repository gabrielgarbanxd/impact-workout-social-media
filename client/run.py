import cmd
from apiService import ApiService

class AppShell(cmd.Cmd):
  intro = 'Bienvenido a la shell de la app. Escribe help o ? para listar los comandos.\n'
  prompt = '(app) '

  def __init__(self):
    super().__init__()
    self.api_service = ApiService()


  # *** Auth ***

  def do_login(self, args):
    """Iniciar sesión"""
    username = input("Nombre de usuario (dejar en blanco si se va a usar email): ")
    email = input("Email (dejar en blanco si se usó nombre de usuario): ")
    password = input("Contraseña: ")
    response = self.api_service.login(username=username if username else None, email=email if email else None, password=password)
    print(response)

  def do_register(self, args):
    """Registrar un nuevo usuario"""
    username = input("Nombre de usuario: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    name = input("Nombre: ")
    role = input("Rol: ")
    gender = input("Género: ")
    birth_date = input("Fecha de nacimiento (YYYY-MM-DD): ")
    response = self.api_service.register(username, email, password, name, role, gender, birth_date)
    print(response)

  def do_verify_email_code(self, args):
    """Verificar el código de email"""
    email = input("Email: ")
    code = input("Código: ")
    response = self.api_service.verify_email_code(email, code)
    print(response)

  def do_resend_verification_code(self, args):
    """Reenviar el código de verificación"""
    email = input("Email: ")
    response = self.api_service.resend_verification_code(email)
    print(response)


  # *** User ***
  def do_get_me(self, args):
    """Obtener mi información de usuario"""
    response = self.api_service.get_me()
    print(response)

  def do_update_me(self, args):
    """Actualizar mi información de usuario"""
    username = input("Nombre de usuario: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    name = input("Nombre: ")
    role = input("Rol: ")
    gender = input("Género: ")
    birthdate = input("Fecha de nacimiento (YYYY-MM-DD): ")
    profile_picture = input("URL de la foto de perfil: ")
    bio = input("Biografía: ")
    links = input("Enlaces (separados por comas): ").split(',')
    private = input("¿Es privado? (s/n): ").lower() == 's'
    vip = input("¿Es VIP? (s/n): ").lower() == 's'
    followers = input("Seguidores (separados por comas): ").split(',')
    body_measures = input("Medidas corporales (separadas por comas): ").split(',')
    training_programs = input("Programas de entrenamiento (separados por comas): ").split(',')
    following = input("Siguiendo a (separados por comas): ").split(',')
    response = self.api_service.update_me(username, email, password, name, role, gender, birthdate, profile_picture, bio, links, private, vip, followers, body_measures, training_programs, following)
    print(response)

  def do_delete_me(self, args):
    """Eliminar mi cuenta de usuario"""
    response = self.api_service.delete_me()
    print(response)

  def do_get_users(self, args):
    """Obtener todos los usuarios"""
    response = self.api_service.get_users()
    print(response)

  def do_get_user(self, args):
    """Obtener un usuario por ID"""
    id = input("ID del usuario: ")
    response = self.api_service.get_user(id)
    print(response)

  def do_get_admin_users(self, args):
    """Obtener todos los usuarios (admin)"""
    response = self.api_service.get_admin_users()
    print(response)

  def do_get_admin_user(self, args):
    """Obtener un usuario por ID (admin)"""
    id = input("ID del usuario: ")
    response = self.api_service.get_admin_user(id)
    print(response)

  def do_delete_admin_user(self, args):
    """Eliminar un usuario por ID (admin)"""
    id = input("ID del usuario: ")
    response = self.api_service.delete_admin_user(id)
    print(response)
  
  # *** Training Programs ***
  def do_get_all_training_programs(self, args):
    """Obtener todos los programas de entrenamiento"""
    response = self.api_service.get_all_training_programs()
    print(response)

  def do_get_one_training_program(self, args):
    """Obtener un programa de entrenamiento por ID"""
    id = input("ID del programa de entrenamiento: ")
    response = self.api_service.get_one_training_program(id)
    print(response)

  def do_create_training_program(self, args):
    """Crear un nuevo programa de entrenamiento"""
    name = input("Nombre: ")
    description = input("Descripción: ")
    exercises = []
    while True:
        exercise_id = input("ID del ejercicio (deja en blanco para terminar): ")
        if not exercise_id:
            break
        sets = []
        while True:
            reps = input("Repeticiones (deja en blanco para terminar): ")
            if not reps:
                break
            weight = input("Peso: ")
            sets.append({"reps": int(reps), "weight": int(weight)})
        exercises.append({"_id": exercise_id, "sets": sets})
    response = self.api_service.create_training_program(name, description, exercises)
    print(response)

  def do_update_training_program(self, args):
    """Actualizar un programa de entrenamiento"""
    id = input("ID del programa de entrenamiento: ")
    name = input("Nombre: ")
    description = input("Descripción: ")
    avg_duration = input("Duración promedio: ")
    avg_volume = input("Volumen promedio: ")
    avg_reps = input("Repeticiones promedio: ")
    avg_sets = input("Sets promedio: ")

    exercises = []
    while True:
        exercise_id = input("ID del ejercicio (deja en blanco para terminar): ")
        if not exercise_id:
            break
        sets = []
        while True:
            reps = input("Repeticiones (deja en blanco para terminar): ")
            if not reps:
                break
            weight = input("Peso: ")
            sets.append({"reps": int(reps), "weight": int(weight)})
        exercises.append({"_id": exercise_id, "sets": sets})

    response = self.api_service.update_training_program(id, name, description, avg_duration, avg_volume, avg_reps, avg_sets, exercises)
    print(response)

  def do_delete_training_program(self, args):
    """Eliminar un programa de entrenamiento"""
    id = input("ID del programa de entrenamiento: ")
    response = self.api_service.delete_training_program(id)
    print(response)


  # *** Trainings ***
  def do_get_all_trainings(self, args):
    """Obtener todos los entrenamientos de un programa"""
    training_program_id = input("ID del programa de entrenamiento: ")
    response = self.api_service.get_all_trainings(training_program_id)
    print(response)

  def do_get_one_training(self, args):
    """Obtener un entrenamiento por ID"""
    training_program_id = input("ID del programa de entrenamiento: ")
    id = input("ID del entrenamiento: ")
    response = self.api_service.get_one_training(training_program_id, id)
    print(response)

  def do_create_training(self, args):
    """Crear un nuevo entrenamiento"""
    training_program_id = input("ID del programa de entrenamiento: ")
    date = input("Fecha (YYYY-MM-DD): ")
    duration = input("Duración: ")
    volume = input("Volumen: ")
    reps = input("Repeticiones: ")
    sets = input("Sets: ")
    exercises = []
    while True:
        exercise_id = input("ID del ejercicio (deja en blanco para terminar): ")
        if not exercise_id:
            break
        sets = []
        while True:
            reps = input("Repeticiones (deja en blanco para terminar): ")
            if not reps:
                break
            weight = input("Peso: ")
            sets.append({"reps": int(reps), "weight": int(weight)})
        exercises.append({"_id": exercise_id, "sets": sets})
    image = input("URL de la imagen: ")
    description = input("Descripción: ")
    visibility = input("Visibilidad: ")
    response = self.api_service.create_training(training_program_id, date, duration, volume, reps, sets, exercises, image, description, visibility)
    print(response)

  def do_update_training(self, args):
    """Actualizar un entrenamiento"""
    training_program_id = input("ID del programa de entrenamiento: ")
    id = input("ID del entrenamiento: ")
    date = input("Fecha (YYYY-MM-DD): ")
    duration = input("Duración: ")
    volume = input("Volumen: ")
    reps = input("Repeticiones: ")
    sets = input("Sets: ")

    exercises = []
    while True:
        exercise_id = input("ID del ejercicio (deja en blanco para terminar): ")
        if not exercise_id:
            break
        sets = []
        while True:
            reps = input("Repeticiones (deja en blanco para terminar): ")
            if not reps:
                break
            weight = input("Peso: ")
            sets.append({"reps": int(reps), "weight": int(weight)})
        exercises.append({"_id": exercise_id, "sets": sets})
    image = input("URL de la imagen: ")
    description = input("Descripción: ")
    visibility = input("Visibilidad: ")
    response = self.api_service.update_training(training_program_id, id, date, duration, volume, reps, sets, exercises, image, description, visibility)
    print(response)

  def do_delete_training(self, args):
    """Eliminar un entrenamiento"""
    training_program_id = input("ID del programa de entrenamiento: ")
    id = input("ID del entrenamiento: ")
    response = self.api_service.delete_training(training_program_id, id)
    print(response)


  # *** Exercises ***
  def do_get_all_exercises(self, args):
    """Obtener todos los ejercicios"""
    muscle = input("Músculo (opcional): ")
    response = self.api_service.get_all_exercises(muscle=muscle if muscle else None)
    print(response)

  def do_get_one_exercise(self, args):
    """Obtener un ejercicio por ID"""
    id = input("ID del ejercicio: ")
    response = self.api_service.get_one_exercise(id)
    print(response)

  def do_create_exercise(self, args):
    """Crear un nuevo ejercicio"""
    name = input("Nombre: ")
    muscle = input("Músculo principal: ")
    description = input("Descripción (opcional): ")
    category = input("Categoría (opcional): ")
    equipment = input("Equipo (opcional): ")
    secondary_muscle = input("Músculo secundario (opcional): ")
    video = input("URL del video (opcional): ")
    image = input("URL de la imagen (opcional): ")
    response = self.api_service.create_exercise(name, muscle, description, category, equipment, secondary_muscle, video, image)
    print(response)

  def do_update_exercise(self, args):
    """Actualizar un ejercicio"""
    id = input("ID del ejercicio: ")
    name = input("Nombre: ")
    muscle = input("Músculo principal: ")
    description = input("Descripción (opcional): ")
    category = input("Categoría (opcional): ")
    equipment = input("Equipo (opcional): ")
    secondary_muscle = input("Músculo secundario (opcional): ")
    video = input("URL del video (opcional): ")
    image = input("URL de la imagen (opcional): ")
    response = self.api_service.update_exercise(id, name, muscle, description, category, equipment, secondary_muscle, video, image)
    print(response)

  def do_delete_exercise(self, args):
    """Eliminar un ejercicio"""
    id = input("ID del ejercicio: ")
    response = self.api_service.delete_exercise(id)
    print(response)

  # *** Posts ***
  def do_get_all_posts(self, args):
    """Obtener todas las publicaciones"""
    response = self.api_service.get_all_posts()
    print(response)

  def do_get_one_post(self, args):
    """Obtener una publicación por ID"""
    id = input("ID de la publicación: ")
    response = self.api_service.get_one_post(id)
    print(response)

  def do_create_post(self, args):
    """Crear una nueva publicación"""
    title = input("Título: ")
    content = input("Contenido: ")
    training_id = input("ID del entrenamiento: ")
    response = self.api_service.create_post(title, content, training_id)
    print(response)

  def do_update_post(self, args):
    """Actualizar una publicación"""
    id = input("ID de la publicación: ")
    title = input("Título: ")
    content = input("Contenido: ")
    training_id = input("ID del entrenamiento: ")
    likes = input("Likes: ")
    comments = input("Comentarios: ")
    response = self.api_service.update_post(id, title, content, training_id, likes, comments)
    print(response)

  def do_delete_post(self, args):
    """Eliminar una publicación"""
    id = input("ID de la publicación: ")
    response = self.api_service.delete_post(id)
    print(response)
  


  # *** Quit *** 
  def do_quit(self, args):
    """Salir de la aplicación"""
    print("Saliendo...")
    return True

if __name__ == '__main__':
  AppShell().cmdloop()