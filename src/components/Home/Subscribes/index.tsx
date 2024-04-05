import { subscriptionType } from "../../../types/subscriptionType";
import EAPlay from "./EAPlay";
import PSPlus from "./PSPlus";

export default function Subscribes({ psSubs, eaSubs }: { psSubs: subscriptionType[], eaSubs: subscriptionType[] }) {
    return (
        <div className="mt-7 flex flex-col gap-7">
            <PSPlus data={psSubs} />
            <EAPlay data={eaSubs} />
        </div>
    )
}
