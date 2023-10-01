import mongoose, { Document, Schema } from 'mongoose';

export interface currentuser {
    id: string;
    email: string;
    name: string;
}
export interface IUser extends Document {
    name: string;
    email: string;
    password: string;
}

const UserSchema: Schema = new Schema({
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true }
});

export const User = mongoose.model<IUser>('User', UserSchema);
