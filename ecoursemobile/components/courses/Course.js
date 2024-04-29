import { View, Text, ActivityIndicator, Image, ScrollView } from "react-native";
import MyStyle from "../../style/MyStyle";
import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { Chip, List, Searchbar } from "react-native-paper";

const Course = () => {
    const [categories, setCategories] = useState(null);
    const [courses, setCourse] = useState([]);
    const [loading, setLoading] = useState(false);
    const [q, setQ] = useState("");
    const [cateId, setCateId] = useState("");

    const loadCates = async () => {
        try {
            let res = await APIs.get(endpoints['categories']);
            setCategories(res.data);
        } catch (ex) {
            console.error(ex);
        }
    }   

    const loadCourses = async () => {
        setLoading(true);
        let url = `${endpoints['courses']}?q=${q}&&category_id=${cateId}`;
        try {
            let res = await APIs.get(url);
            setCourse(res.data.results);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadCates();
    }, []);

    useEffect(() => {
        loadCourses();
    }, [q, cateId]);

    return (
        <View style={MyStyle.container}>
            <View style={[MyStyle.row, MyStyle.wrap]}>
            <Chip mode={cateId?"outlined":"flat"} onPress={() => setCateId("")} style={MyStyle.margin} icon="tag">Tất cả</Chip>
                {categories===null?<ActivityIndicator/>:<>
                    {categories.map(c => <Chip mode={cateId===c.id?"flat":"outlined"} style={MyStyle.margin} key={c.id} icon="tag" onPress={() => setCateId(c.id)}>{c.name}</Chip>)}
                </>}
            </View>

            <View>
                <Searchbar placeholder="Search course..." value={q} onChangeText={setQ} />
            </View>

            <ScrollView style={MyStyle.margin}>
                {loading && <ActivityIndicator/>}
                {courses.map(c => <List.Item key={c.id} title={c.name} description= {c.created_date} 
                    left={() => <Image style={MyStyle.avatar} source= {{uri: c.image}} />} />)
                    }
            </ScrollView>
        </View>
    );
};

export default Course;