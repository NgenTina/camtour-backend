import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, CreateDateColumn } from 'typeorm';
import { Conversation } from './conversation.entity';

@Entity()
export class Message {
  @PrimaryGeneratedColumn()
  id: number;

  @Column('text')
  content: string;

  @Column({
    type: 'enum',
    enum: ['user', 'ai'],
  })
  sender: 'user' | 'ai';

  @ManyToOne(() => Conversation, conversation => conversation.messages, {
    onDelete: 'CASCADE', // This ensures messages are deleted when conversation is deleted
  })
  conversation: Conversation;

  @CreateDateColumn()
  timestamp: Date;
}