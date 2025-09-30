import { IsString, IsOptional, IsNumber } from 'class-validator';

export class CreateConversationDto {
  @IsString()
  @IsOptional()
  title: string;

  @IsNumber()
  userId: number;
}