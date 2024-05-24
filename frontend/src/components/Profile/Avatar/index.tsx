import avatar1 from '@avatars/1.jpg'
import avatar2 from '@avatars/2.jpg'
import avatar3 from '@avatars/3.jpg'
import avatar4 from '@avatars/4.jpg'
import avatar5 from '@avatars/5.jpg'
import avatar6 from '@avatars/6.jpg'
import avatar7 from '@avatars/7.jpg'
import avatar8 from '@avatars/8.jpg'
import avatar9 from '@avatars/9.jpg'
import avatar10 from '@avatars/10.jpg'
import avatar11 from '@avatars/11.jpg'
import avatar12 from '@avatars/12.jpg'
import avatar13 from '@avatars/13.jpg'
import avatar14 from '@avatars/14.jpg'
import avatar15 from '@avatars/15.jpg'
import avatar16 from '@avatars/16.jpg'
import avatar17 from '@avatars/17.jpg'
import avatar18 from '@avatars/18.jpg'
import avatar19 from '@avatars/19.jpg'
import avatar20 from '@avatars/20.jpg'
import { memo } from 'react'


const avatars = [
    avatar1, avatar2, avatar3, avatar4, avatar5, avatar6, avatar7, avatar8, avatar9, avatar10,
    avatar11, avatar12, avatar13, avatar14, avatar15, avatar16, avatar17, avatar18, avatar19, avatar20,
]

const Avatar = memo(() => {
    const randomAvatar = Math.floor(Math.random() * avatars.length);
    return (
        <img src={avatars[randomAvatar]} className="w-14 h-14 rounded-full mr-6" />
    );
});

export default Avatar;
