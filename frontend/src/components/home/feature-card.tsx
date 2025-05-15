import { ReactNode } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface FeatureCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  buttonLabel: string;
  onClick: () => void;
}

export function FeatureCard({
  icon,
  title,
  description,
  buttonLabel,
  onClick,
}: FeatureCardProps) {
  return (
    <Card className="flex flex-col items-center text-center shadow-md p-6">
      <CardHeader className="flex flex-col items-center">
        <div className="text-blue-600 bg-blue-100 rounded-full p-3 mb-2">
          {icon}
        </div>
        <CardTitle className="text-lg font-bold">{title}</CardTitle>
      </CardHeader>
      <CardContent className="text-muted-foreground mb-4 text-sm">
        {description}
      </CardContent>
      <Button onClick={onClick}>{buttonLabel}</Button>
    </Card>
  );
}
