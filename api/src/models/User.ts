import mongoose from 'mongoose';
import bcrypt from 'bcrypt';

export interface IUser extends mongoose.Document {
    email: string;
    password: string;
    comparePassword: (password: string) => Promise<boolean>;
}

const userSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
});

userSchema.pre<IUser>('save', async function(next) {
    if (this.isModified('password')) {
        this.password = await bcrypt.hash(this.password, 10);
    }
    next();
});

userSchema.methods.comparePassword = function(password: string): Promise<boolean> {
    return bcrypt.compare(password, this.password);
}

export const User = mongoose.model<IUser>('User', userSchema);
