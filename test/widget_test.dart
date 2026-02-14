import 'package:flutter_test/flutter_test.dart';
import 'package:wislla/main.dart';

void main() {
  testWidgets('Wislla App smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const WisllaApp());

    // Verify that our welcome message is present.
    expect(find.text('Welcome to Wislla'), findsOneWidget);
  });
}
