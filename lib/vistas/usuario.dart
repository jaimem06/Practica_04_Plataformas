import 'package:flutter/material.dart';
import 'package:practica_04_movil/controller/Coneccion.dart';
import 'package:practica_04_movil/models/ResponseGeneric.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:practica_04_movil/main.dart'; // Asegúrate de importar el archivo donde se define la página de inicio

class UsuarioVista extends StatefulWidget {
  const UsuarioVista({super.key});

  @override
  UsuarioVistaState createState() => UsuarioVistaState();
}

class UsuarioVistaState extends State<UsuarioVista> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _correoController = TextEditingController();
  final TextEditingController _claveController = TextEditingController();
  final Connection _conexion = Connection();
  final FlutterSecureStorage _secureStorage = FlutterSecureStorage();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _cargarDatosUsuario();
  }

  Future<void> _cargarDatosUsuario() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final ResponseGeneric response = await _conexion.getUsuario();
      if (response.code == '200' && response.datos.isNotEmpty) {
        final userData = response.datos[0];
        setState(() {
          _correoController.text = userData['correo'];
          _claveController.text = userData['clave'];
        });
        print('Datos del usuario cargados: $userData');
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: ${response.msg}')),
        );
        print('Error en la respuesta del servidor: ${response.msg}');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar datos del usuario: $e')),
      );
      print('Error al cargar datos del usuario: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _editarDatos() {
    if (_formKey.currentState!.validate()) {
      // Aquí puedes manejar la lógica de edición de datos
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Datos editados exitosamente')),
      );
    }
  }

  void _cerrarSesion() async {
    await _secureStorage.delete(key: 'token'); // Elimina el token guardado
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(
          builder: (context) => MyApp()), // Redirige a la página de inicio
      (Route<dynamic> route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Editar Datos'),
      ),
      body: Center(
        child: _isLoading
            ? CircularProgressIndicator()
            : Padding(
                padding: const EdgeInsets.all(16.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Icon(
                        Icons.person,
                        size: 100,
                        color: Colors.blueAccent,
                      ),
                      SizedBox(height: 20),
                      TextFormField(
                        controller: _correoController,
                        decoration: InputDecoration(labelText: 'Correo'),
                        keyboardType: TextInputType.emailAddress,
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Por favor ingrese su correo';
                          }
                          return null;
                        },
                      ),
                      TextFormField(
                        controller: _claveController,
                        decoration: InputDecoration(labelText: 'Clave'),
                        obscureText: true,
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Por favor ingrese su clave';
                          }
                          return null;
                        },
                      ),
                      SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: _editarDatos,
                        child: Text('Editar Datos'),
                      ),
                      SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: _cerrarSesion,
                        child: Text('Cerrar Sesión'),
                        style: ElevatedButton.styleFrom(
                            // primary: Colors.red, // Color del botón de cerrar sesión
                            ),
                      ),
                    ],
                  ),
                ),
              ),
      ),
    );
  }
}
