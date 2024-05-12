import { createStackNavigator } from "@react-navigation/stack";
import Course from "./components/courses/Course";
import Lesson from "./components/courses/Lesson";
import { NavigationContainer } from "@react-navigation/native";
import LessonDetails from "./components/courses/LessonDetails";

const Stack = createStackNavigator();

const MyStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Course" component={Course} />
      <Stack.Screen name="Lesson" component={Lesson} />
      <Stack.Screen name="LessonDetails" component={LessonDetails} />
    </Stack.Navigator>
  );
}

const App = () => {
  return (
    // tất cả những thứ muốn điều hướng phải đặt trong NavigationContainer
    <NavigationContainer>
      {<MyStack /> }
    </NavigationContainer>
  );
}

export default App;