import { Image } from "react-native";
import MyStyle from "../../style/MyStyle";
import { List } from "react-native-paper";

const Item = ({instance}) => {
    return (<List.Item title={instance.subject} description= {instance.created_date} 
                left={() => <Image style={MyStyle.avatar} source= {{uri: instance.image}} />} />
            );
}

export default Item;