import { ScrollView, View, Text, ActivityIndicator, useWindowDimensions, Image } from "react-native";
import MyStyle from "../../style/MyStyle";
import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { Card, Chip } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import { isCloseToBottom } from "../utils/Utils";

const LessonDetails = ({route}) => {
    const [lesson, setLesson] = useState(null);
    const lessonId = route.params?.lessonId;
    const { width } = useWindowDimensions();
    const [comments, setComments] = useState(null);

    const loadLesson = async () => {
        try {
            let res = await APIs.get(endpoints['lesson-detail'](lessonId));
            setLesson(res.data);
        } catch(ex){
            console.error(ex);
        }
    }

    const loadComments = async () => {
        try {
            let res = await APIs.get(endpoints['comments'](lessonId));
            setComments(res.data);            
        } catch(ex) {
            console.error(ex);
        }
    }

    useEffect(() => {
        loadLesson();
    }, [lessonId]);

    // lazy
    // kéo xuống cuối trang mới bắt đầu nạp comments 
    const loadMoreInfo = ({nativeEvent}) => { 
        if (!comments && isCloseToBottom(nativeEvent)) {
            loadComments();
        }
    }


    return (
        <View style={MyStyle}>
            <ScrollView onScroll={loadMoreInfo}>
                {lesson===null?<ActivityIndicator />:<>
                <Card>
                    <Card.Title title={lesson.subject} titleStyle={MyStyle.subject} />
                    <Card.Cover source={{ uri: lesson.image }} />

                    <Card.Content>
                        <View style={MyStyle.row}>
                            {lesson.tags.map(t => <Chip icon='tag' style={MyStyle.margin} key={t.id}>{t.name}</Chip>)}
                        </View>

                        <Text variant="bodyMedium">
                            <RenderHTML contentWidth={width} source={{html: lesson.content}} />
                        </Text>

                    </Card.Content>
                </Card>
                </>}

                <View>

                </View>

                <View>
                    {comments && <>
                        {comments.map(c => <List.Item key={c.id}
                            title={c.content}
                            description = {c.created_date}
                            left={() => <Image source={{uri: c.user.avatar}} style={MyStyle.avatar} />}
                        />)}
                    </>}
                    
                </View>

            </ScrollView>
            
        </View>
    )
};

export default LessonDetails;