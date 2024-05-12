import { View, Text, ActivityIndicator, Image, ScrollView, TouchableOpacity } from "react-native";
import MyStyle from "../../style/MyStyle";
import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { Chip, List, Searchbar } from "react-native-paper";
import Item from "../utils/Item";
import { isCloseToBottom } from "../utils/Utils";

const Course = ({navigation}) => {
    const [categories, setCategories] = useState(null);
    const [courses, setCourse] = useState([]);
    const [loading, setLoading] = useState(false);
    const [q, setQ] = useState("");
    const [cateId, setCateId] = useState("");
    const [page, setPage] = useState(1)

    const loadCates = async () => {
        try {
            let res = await APIs.get(endpoints['categories']);
            setCategories(res.data);
        } catch (ex) {
            console.error(ex);
        }
    }   

    const loadCourses = async () => {
        if (page > 0){
            setLoading(true);
            let url = `${endpoints['courses']}?q=${q}&&category_id=${cateId}&&page=${page}`;
            try {
                let res = await APIs.get(url);
                if (page === 1)
                    setCourse(res.data.results);
                else
                setCourse(current => {
                    return [...current, ...res.data.results] //chen them du lieu vao trang hien tai
                });
    
                if (!res.data.next)
                    setPage(0);
    
            } catch (ex) {
                console.error(ex);
            } finally {
                setLoading(false);
            }
        }
        
    }

    useEffect(() => {
        loadCates();
    }, []);

    useEffect(() => {
        loadCourses();
    }, [q, cateId, page]);

    const loadMore = ({nativeEvent}) => {
    if (!loading && page > 0 && isCloseToBottom(nativeEvent)){
        setPage(page + 1);
    }
    }

    const search = (value, callback) => {
        setPage(1);
        callback(value);
    }

    return (
        <View style={MyStyle.container}>
            <View style={[MyStyle.row, MyStyle.wrap]}>
                <Chip mode={!cateId?"outlined":"flat"} onPress={() => search("", setCateId)} style={MyStyle.margin} icon="shape-plus">Tất cả</Chip>
                {categories===null?<ActivityIndicator/>:<>
                    {categories.map(c => <Chip mode={c.id===cateId?"outlined":"flat"} key={c.id} onPress={() => search(c.id, setCateId)} style={MyStyle.margin} icon="shape-plus">{c.name}</Chip>)}
                </>}
            </View>

            <View>
                <Searchbar placeholder="Search course..." value={q} onChangeText={setQ} />
            </View>

            <ScrollView style={MyStyle.margin} onScroll={loadMore}>
                {loading && <ActivityIndicator/>}
                {courses.map(c => <TouchableOpacity key={c.id} onPress={() => navigation.navigate('Lesson', {'courseId': c.id})}>
                    <Item instance={c} />
                </TouchableOpacity>)}
            </ScrollView>
        </View>
    );
};

export default Course;