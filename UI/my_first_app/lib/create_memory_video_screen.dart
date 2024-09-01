import 'package:flutter/material.dart';

class CreateMemoryVideoScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Background Image
          Positioned.fill(
            child: Image.asset(
              'assets/background_image.png', // Replace with your background image
              fit: BoxFit.cover,
            ),
          ),
          // Card View with Action Button
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              margin: EdgeInsets.all(16.0),
              padding: EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16.0),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black26,
                    blurRadius: 10.0,
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'Create Your Memory Video',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Transform your travel experiences into personalized cinematic stories using AI.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 16),
                  ),
                  SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      // Navigate to the MediaTabLayoutScreen
                      //Navigator.pushNamed(context, '/media-tab-layout');
                      //Navigator.pushNamed(context, '/media-selection-layout');
                      //Navigator.pushNamed(context, '/video-player-layout');
                      Navigator.pushNamed(context, '/milestone');
                    },
                    child: Text("Let's start"),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
