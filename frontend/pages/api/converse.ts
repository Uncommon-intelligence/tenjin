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
    const id = req.body.conversationId || uuidV4();
    const { data } = await axios.post(`https://timmy-dev.ngrok.io/proxy/8000/web/${id}`, {
        conversationId: id,
        input: req.body.input,
    })

    res.status(200).json({ data });
}
