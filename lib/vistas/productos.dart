import 'package:flutter/material.dart';
import 'package:practica_04_movil/controller/Coneccion.dart';
import 'package:practica_04_movil/models/ResponseGeneric.dart';

class Vista_Productos extends StatefulWidget {
  const Vista_Productos({super.key});

  @override
  Vista_ProductosState createState() => Vista_ProductosState();
}

class Vista_ProductosState extends State<Vista_Productos> {
  final Connection conexion = Connection();
  List<dynamic> productos = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    cargarProductos();
  }

  void cargarProductos() async {
    try {
      final ResponseGeneric response = await conexion.getProductos();
      if (response.code == '200' && response.datos != null) {
        setState(() {
          productos = response.datos;
          isLoading = false;
        });
      } else {
        setState(() {
          isLoading = false;
        });
        print('Error: ${response.msg}');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      print('Error al cargar productos: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Productos'),
        backgroundColor: Colors.blue[800],
      ),
      body: Center(
        child: isLoading
            ? CircularProgressIndicator()
            : Padding(
                padding: const EdgeInsets.all(8.0),
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2, // Número de columnas
                    crossAxisSpacing: 8.0,
                    mainAxisSpacing: 8.0,
                  ),
                  itemCount: productos.length,
                  itemBuilder: (context, index) {
                    var producto = productos[index];
                    return Card(
                      color:
                          Colors.blue[50], // Fondo azul suave para la tarjeta
                      elevation: 5,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              producto['nombre'],
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.blue[900], // Color del texto
                              ),
                            ),
                            SizedBox(height: 10),
                            Text(
                              'Cantidad: ${producto['cantidad']}',
                              style: TextStyle(color: Colors.blue[800]),
                            ),
                            Text(
                              'Estado: ${producto['estado']}',
                              style: TextStyle(color: Colors.blue[800]),
                            ),
                            Text(
                              'Caducidad: ${producto['fecha_caducidad']}',
                              style: TextStyle(color: Colors.blue[800]),
                            ),
                            Text(
                              'Precio: \$${producto['precio_unitario']}',
                              style: TextStyle(color: Colors.blue[800]),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
      ),
    );
  }
}
