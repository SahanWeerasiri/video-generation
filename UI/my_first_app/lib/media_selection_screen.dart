import 'package:flutter/material.dart';

class MediaSelectionScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Select Files'),
      ),
      body: GridView.builder(
        padding: EdgeInsets.all(8.0),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          crossAxisSpacing: 8.0,
          mainAxisSpacing: 8.0,
        ),
        itemCount: 12, // Replace with actual media items count
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              // Handle media selection
            },
            child: Stack(
              children: [
                Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8.0),
                    image: DecorationImage(
                      image: AssetImage('assets/media_thumbnail.jpg'), // Replace with media thumbnail
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                Align(
                  alignment: Alignment.topRight,
                  child: Icon(Icons.check_circle_outline, color: Colors.white),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
