import { IsString, IsNumber, IsEnum } from 'class-validator';

export class CreateMessageDto {
  @IsString()
  content: string;

  @IsEnum(['user', 'ai'])
  sender: 'user' | 'ai';

  @IsNumber()
  conversationId: number;
}