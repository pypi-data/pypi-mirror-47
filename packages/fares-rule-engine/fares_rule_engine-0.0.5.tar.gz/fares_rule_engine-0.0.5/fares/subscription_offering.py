from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from rule_engine.operator import In, Equals
from rule_engine.rule import RuleSet, Rule
from typing import List, Union


@dataclass(frozen=True)
class InterClusterApplicability:
    origin_cluster_id: str
    destination_cluster_id: str
    session: str


@dataclass
class ZoneWideApplicability:
    zone_id: str


@dataclass
class Applicability:
    type: str
    rules: List[Union[InterClusterApplicability, ZoneWideApplicability]]


class SubscriptionType(Enum):
    TRIAL = "TRIAL"
    STANDARD = "STANDARD"


@dataclass
class SubscriptionOffering:
    id: str
    name: str
    rides: int
    currency: str
    validity_in_days: int
    is_carry_forward: bool
    activation_date: datetime
    deactivation_date: datetime
    zone_id: str
    amount: int
    subscription_type: SubscriptionType
    applicability: Applicability
    created_at: datetime

    @property
    def applicability_type(self):
        return self.applicability.type

    @property
    def applicability_rules(self):
        return self.applicability.rules

    def usage_applicability_rules(self) -> RuleSet:
        rules = []
        if self.applicability_type == "ZONE_WIDE":
            rule = Rule(
                "slot.zone_id", In(), [a.zone_id for a in self.applicability_rules]
            )
            rules.append(rule)
        elif self.applicability_type == "INTER_CLUSTER":
            rule = Rule(
                "slot.od_cluster_session",
                In(),
                [
                    (app.origin_cluster_id, app.destination_cluster_id, app.session)
                    for app in self.applicability_rules
                ],
            )
            rules.append(rule)

        return RuleSet(rules)

    def purchase_applicability_rules(self) -> RuleSet:

        if SubscriptionType.STANDARD == self.subscription_type:
            return RuleSet([])

        return RuleSet([Rule("user.pass_purchase_count", Equals(), 0)])

    @classmethod
    def from_json(cls, dikt):
        # TODO : This was done to allow older subscriptions to run according to previous system.Remove it.
        def _inter_cluster(rules):
            applicability_rules = []

            for app in rules:
                morning = InterClusterApplicability(
                    app["origin_cluster_id"], app["destination_cluster_id"], "MORNING"
                )
                evening = InterClusterApplicability(
                    app["origin_cluster_id"], app["destination_cluster_id"], "EVENING"
                )
                applicability_rules.append(morning)
                applicability_rules.append(evening)

            return applicability_rules

        def _zone_wide(rules):
            return [ZoneWideApplicability(rule["zone_id"]) for rule in rules]

        def _applicability(dikt):
            type = dikt["type"]
            rules = dikt["rules"]
            if type == "ZONE_WIDE":
                return Applicability("ZONE_WIDE", _zone_wide(rules))
            elif type == "INTER_CLUSTER":
                return Applicability("INTER_CLUSTER", _inter_cluster(rules))

        return SubscriptionOffering(
            id=dikt["id"],
            name=dikt["name"],
            rides=dikt["rides"],
            currency=dikt["currency"],
            validity_in_days=dikt["validity_in_days"],
            is_carry_forward=dikt["is_carry_forward"],
            activation_date=dikt["activation_date"],
            deactivation_date=dikt["deactivation_date"],
            zone_id=dikt["zone_id"],
            amount=dikt["amount"],
            subscription_type=SubscriptionType(dikt["subscription_type"]),
            applicability=_applicability(dikt["applicability"]),
            created_at=datetime.fromisoformat(dikt["created_at"]),
        )
