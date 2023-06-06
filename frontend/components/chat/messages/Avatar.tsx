import React, { FC } from "react";

interface AvatarProps {
    user?: string;
}

const Avatar: FC<AvatarProps> = (props) => {
    const { user: _ } = props;

    return <div className="bg-blue-400 w-[30px] h-[30px] rounded-[15px]" />;
};

export default Avatar;
