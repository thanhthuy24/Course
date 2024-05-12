import { View, Text, TouchableOpacity } from "react-native";
import MyStyle from "../../style/MyStyle";
import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { ActivityIndicator } from "react-native-paper";
import Item from "../utils/Item";

const Lesson = ({navigation, route}) => {
    const [lessons, setLessons] = useState(null);
    // kí pháp .params.?courseId means: nếu nó null thì kết thúc, còn ko null sẽ lấy courseId ra
    // params có khả năng bị null
    const courseId = route.params?.courseId;
    
    const loadLessons = async () => {
        // fetch API
        try {
            let res = await APIs.get(endpoints['lessons'](courseId));
            setLessons(res.data);
        } catch (ex) {
            console.error(ex);
        }
    }

    useEffect(() => {
        loadLessons();
    }, [courseId]);

    return (
        <View style={MyStyle.container}>
           {lessons===null?<ActivityIndicator />:<>
            {lessons.map(l => <TouchableOpacity key={l.id} onPress={() => navigation.navigate('LessonDetails', {'lessonId':l.id})}>
                <Item instance={l}/>
            </TouchableOpacity>)}
           </>}
        </View>
    );
}

export default Lesson;

