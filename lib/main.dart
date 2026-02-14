import 'package:flutter/material.dart';

void main() {
  runApp(const WisllaApp());
}

class WisllaApp extends StatelessWidget {
  const WisllaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Wislla App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const WisllaHomePage(),
    );
  }
}

class WisllaHomePage extends StatelessWidget {
  const WisllaHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Wislla App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Welcome to Wislla',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            Image.asset(
              'assets/logo_v2.png',
              width: 100,
              height: 100,
              errorBuilder: (context, error, stackTrace) {
                return const Icon(Icons.image_not_supported, size: 100);
              },
            ),
          ],
        ),
      ),
    );
  }
}
