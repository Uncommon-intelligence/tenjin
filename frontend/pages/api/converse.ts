// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import axios from "axios";
import type { NextApiRequest, NextApiResponse } from "next";
import { v4 as uuidV4 } from "uuid";

type Data = {
    data: any;
};

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
) {
    const { conversationId: conversation_id, input } = req.body
    const { data } = await axios.post(`https://timmy.ngrok.io/qa`, { conversation_id, input })

    res.status(200).json(data)
}
